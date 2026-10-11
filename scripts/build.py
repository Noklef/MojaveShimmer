import argparse
from pathlib import Path
import struct
import zipfile


def validate_texture_helpers(blocks, block_types, strings):
    """Check FNV texture-controller layouts independently of the NIF writer.

    Layouts: https://github.com/niftools/nifxml/blob/develop/nif.xml
    FNV pairing: https://geckwiki.com/index.php?title=NiTexturingProperty
    """
    def object_end(block):
        return 12 + 4 * struct.unpack_from("<I", block, 4)[0]

    for index, (block, kind) in enumerate(zip(blocks, block_types)):
        if kind != "NiTexturingProperty":
            continue
        pos = object_end(block)
        count = struct.unpack_from("<I", block, pos + 2)[0]
        pos += 6
        if not 1 <= count <= 12:
            raise ValueError("Invalid NIF texture-slot count")
        sources = []
        for slot in range(count):
            present = block[pos]
            pos += 1
            if present not in (0, 1):
                raise ValueError("Invalid NIF texture-slot marker")
            if not present:
                continue
            source = struct.unpack_from("<i", block, pos)[0]
            sources.append(source)
            # FNV TexDesc: source, flags, transform marker, optional transform.
            transformed = block[pos + 6]
            if transformed not in (0, 1):
                raise ValueError("Invalid NIF texture-transform marker")
            pos += 7 + (32 if transformed else 0)
            if slot == 5:
                pos += 24  # Bump luminance and matrix.
            elif slot == 7:
                pos += 4  # Parallax offset.
        # The haze helper has no shader-map textures. Require exact consumption:
        # old PyFFI wrote nine slot markers even when Texture Count was seven.
        if pos + 4 != len(block) or struct.unpack_from("<I", block, pos)[0] != 0:
            raise ValueError("NIF texture count does not match its serialized slots")

        owners = []
        for shape, shape_kind in zip(blocks, block_types):
            if shape_kind != "NiTriShape":
                continue
            prop_pos = object_end(shape) + 56  # Flags and local transform.
            prop_count = struct.unpack_from("<I", shape, prop_pos)[0]
            properties = struct.unpack_from(f"<{prop_count}i", shape, prop_pos + 4)
            if index in properties:
                owners.append(properties)
        if not owners:
            raise ValueError("NIF texture helper is not attached to a shape")
        for properties in owners:
            shaders = [i for i in properties if block_types[i] == "BSShaderNoLightingProperty"]
            if len(shaders) != 1:
                raise ValueError("NIF texture helper requires a NoLighting shader")
            shader = blocks[shaders[0]]
            shader_pos = object_end(shader)
            if struct.unpack_from("<I", shader, shader_pos + 2)[0] != 33:
                raise ValueError("NIF texture helper requires SHADER_NOLIGHTING")
            length = struct.unpack_from("<I", shader, shader_pos + 22)[0]
            filename = bytes(shader[shader_pos + 26:shader_pos + 26 + length])
            for source in sources:
                if not 0 <= source < len(blocks) or block_types[source] != "NiSourceTexture":
                    raise ValueError("Invalid NIF helper texture reference")
                source_block = blocks[source]
                name_id = struct.unpack_from("<i", source_block, object_end(source_block) + 1)[0]
                if not 0 <= name_id < len(strings) or strings[name_id] != filename:
                    raise ValueError("NIF helper texture must match its NoLighting shader")


def package_mesh(data, debug=False):
    """Validate the FNV mesh and optionally patch its debug shader/texture."""
    header = b"Gamebryo File Format, Version 20.2.0.7\n"
    if not data.startswith(header):
        raise ValueError("Build requires a Fallout: New Vegas NIF")
    pos = len(header)

    def take(fmt):
        nonlocal pos
        values = struct.unpack_from("<" + fmt, data, pos)
        pos += struct.calcsize("<" + fmt)
        return values

    if (take("I")[0], take("B")[0], take("I")[0]) != (0x14020007, 1, 11):
        raise ValueError("Unexpected NIF version")
    count = take("I")[0]
    if take("I")[0] != 34:
        raise ValueError("Unexpected NIF Bethesda version")
    for _ in range(3):
        length = take("B")[0]
        pos += length
    types = []
    for _ in range(take("H")[0]):
        length = take("I")[0]
        types.append(data[pos:pos + length].decode("ascii"))
        pos += length
    indices = take(f"{count}H")
    sizes_pos = pos
    sizes = take(f"{count}I")
    string_count = take("I")[0]
    take("I")  # Maximum string length.
    strings = []
    for _ in range(string_count):
        length = take("I")[0]
        strings.append(data[pos:pos + length])
        pos += length
    pos += 4 + 4 * struct.unpack_from("<I", data, pos)[0]  # Groups.
    output_header = bytearray(data[:pos])
    blocks = []
    shaders_changed = textures_changed = 0
    for index, (type_id, size) in enumerate(zip(indices, sizes)):
        if type_id >= len(types) or pos + size > len(data):
            raise ValueError("Invalid NIF block table")
        block = bytearray(data[pos:pos + size])
        pos += size
        if debug and types[type_id] == "BSShaderPPLightingProperty":
            # NiObjectNET: name, extra-data count/list, controller; then flags
            # (ushort), shader type (uint), and Shader Flags (uint).
            extra_count = struct.unpack_from("<I", block, 4)[0]
            flags_pos = 18 + 4 * extra_count
            flags = struct.unpack_from("<I", block, flags_pos)[0]
            # Clear Refraction and Fire_Refraction only; preserve other flags.
            struct.pack_into("<I", block, flags_pos, flags & ~((1 << 15) | (1 << 16)))
            shaders_changed += 1
        elif debug and types[type_id] == "BSShaderTextureSet":
            texture_count, length = struct.unpack_from("<II", block)
            diffuse = bytes(block[8:8 + length])
            if texture_count and diffuse.lower().replace(b"/", b"\\") == b"textures\\mojaveshimmer\\shimmer_d.dds":
                replacement = b"textures\\mojaveshimmer\\shimmer_d_debug.dds"
                block[4:8 + length] = struct.pack("<I", len(replacement)) + replacement
                textures_changed += 1
        struct.pack_into("<I", output_header, sizes_pos + index * 4, len(block))
        blocks.append(block)
    validate_texture_helpers(blocks, [types[i] for i in indices], strings)
    if debug and (not shaders_changed or not textures_changed):
        raise ValueError("Debug NIF is missing the haze shader or diffuse texture")
    return bytes(output_header) + b"".join(blocks) + data[pos:]


def debug_mesh(data):
    return package_mesh(data, debug=True)


def main():
    parser = argparse.ArgumentParser(description="Build the Mojave Shimmer package.")
    parser.add_argument("--debug", action="store_true",
                        help="Use the debug diffuse texture and disable refraction in the packaged NIF")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    source = root / "src"
    mesh_path = Path("Meshes/mojaveshimmer/mojaveshimmer_cylinder.nif")
    mesh = source / mesh_path
    if not mesh.is_file():
        raise FileNotFoundError(f"Missing mesh: {mesh}")
    debug_texture = Path("Textures/mojaveshimmer/shimmer_d_debug.dds")
    mesh_data = package_mesh(mesh.read_bytes())
    if args.debug:
        if not (source / debug_texture).is_file():
            raise FileNotFoundError(f"Missing debug texture: {source / debug_texture}")
        mesh_data = debug_mesh(mesh_data)
    name = "MojaveShimmer_debug.zip" if args.debug else "MojaveShimmer.zip"
    output = root / "dist" / name
    output.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(source)
            if relative.parts[0] == "Meshes" and relative != mesh_path:
                continue
            if relative == debug_texture and not args.debug:
                continue
            if relative == mesh_path:
                archive.writestr(relative.as_posix(), mesh_data)
            else:
                archive.write(path, relative.as_posix())
    print(f"Built {output} (mesh: {mesh.name})")


if __name__ == "__main__":
    main()
