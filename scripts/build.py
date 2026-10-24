"""Zip src/ into dist/MojaveShimmer.zip (the zip root is the game's Data folder).

    python scripts/build.py

Files are copied as-is. The only check is that the mesh is an FNV NIF that still has the block names
the scripts look up, since JIP's NIF commands fail silently if a Blender export renamed one.
Stdlib only, so CI can run it on a bare Python install.
"""
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "src"
OUTPUT = ROOT / "dist" / "MojaveShimmerDebug.zip"

MESH = Path("Meshes/mojaveshimmer/mojaveshimmer_cylinder.nif")  # Relative to src/, the only mesh that ships
NIF_HEADER = b"Gamebryo File Format, Version 20.2.0.7\n"
SCRIPT_BLOCK_NAMES = ["MojaveShimmerRoot", "MojaveShimmerCylinder", "MojaveShimmerStrengthControl", "MojaveShimmerDebugWireframe"]


def check_mesh(path):
    if not path.is_file():
        sys.exit(f"Build failed: missing mesh {path}")
    data = path.read_bytes()
    if not data.startswith(NIF_HEADER):
        sys.exit(f"Build failed: {path.name} isn't a Fallout: New Vegas NIF (20.2.0.7)")
    missing = [name for name in SCRIPT_BLOCK_NAMES if name.encode("ascii") not in data]
    if missing:
        sys.exit(f"Build failed: {path.name} is missing block(s) the scripts use: {', '.join(missing)}")


def main():
    check_mesh(SOURCE / MESH)
    OUTPUT.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(SOURCE.rglob("*")):
            relative = path.relative_to(SOURCE)
            # Everything under src/ ships, except meshes other than the cylinder, and texture work files (only .dds ship)
            if path.is_file() and (relative.parts[0] != "Meshes" or relative == MESH) \
                    and (relative.parts[0] != "Textures" or path.suffix.lower() == ".dds"):
                archive.write(path, relative.as_posix())
    print(f"Built {OUTPUT}")


if __name__ == "__main__":
    main()
