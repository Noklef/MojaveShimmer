# Mojave Shimmer add strength trick
# A hacky way to add intensity to the cylinder we're using
from pathlib import Path

import bpy
from nifgen.formats.nif import NifFile, classes as Nif# Library to use from the NIF tools addon

nif_path = str(Path(bpy.data.filepath).parent.parent / "mojaveshimmer_cylinder.nif")
data = NifFile.from_path(nif_path)
root = data.roots[0]

# Get the info from the nif we need
cylinder = next(c for c in root.children if c.name == "MojaveShimmerCylinder")
shader = next(p for p in cylinder.properties if isinstance(p, Nif.BSShaderPPLightingProperty))
strength = shader.refraction_strength # Blender shader refraction
normal_map = shader.texture_set.textures[1] #[1] is the normal map we're using

# Create the `NiFloatData` block we need for the refraction
keys = Nif.NiFloatData(data)
keys.data.num_keys = 2 
keys.data.reset_field("keys")
keys.data.keys[1].time = 1.0
for key in keys.data.keys:
    key.value = strength

def controller(controller_type):
    # Each controller gets its own interpolator, but both interpolators read the shared keys
    interpolator = Nif.NiFloatInterpolator(data)
    interpolator.value = strength
    interpolator.data = keys
    controller = controller_type(data)
    controller.flags = Nif.TimeControllerFlags.from_value(0x48)
    controller.start_time = 0.0 
    controller.stop_time = 1.0
    controller.interpolator = interpolator
    return controller

# add_controller also points the controller's target back at the shader
shader.add_controller(controller(Nif.BSRefractionStrengthController))

# The helper: a hidden triangle whose texture transform controller is what SetTextureTransformKey
# edits (ctrlIdx 0). All it does itself is shift its own unseen texture's U.
texture = Nif.NiSourceTexture(data)
texture.file_name = normal_map   # same file as the cylinder's normal map, as shipped
# nifgen defaults to palettised / default mipmaps, the shipped helper has these
texture.format_prefs.pixel_layout = Nif.PixelLayout.LAY_DEFAULT
texture.format_prefs.use_mipmaps = Nif.MipMapFormat.MIP_FMT_YES

# A NiTextureTransformController has to sit on a NiTexturingProperty, which is the only reason
# the helper has one. Mode and slot count match the shipped helper (nifgen: replace, 7 slots).
texturing = Nif.NiTexturingProperty(data)
texturing.flags.apply_mode = Nif.ApplyMode.APPLY_MODULATE
texturing.texture_count = 9
texturing.has_base_texture = True
texturing.base_texture.source = texture
texturing.base_texture.has_texture_transform = True   # the transform the controller shifts
texturing.add_controller(controller(Nif.NiTextureTransformController))

unlit = Nif.BSShaderNoLightingProperty(data)
unlit.shader_type = Nif.BSShaderType.SHADER_NOLIGHTING
unlit.shader_flags = Nif.BSShaderFlags.from_value(0)     # nifgen defaults to z-buffer flags,
unlit.shader_flags_2 = Nif.BSShaderFlags2.from_value(0)  # the shipped helper has none
unlit.file_name = normal_map

# One tiny triangle at the origin, just so the helper is a real shape
geometry = Nif.NiTriShapeData(data)
geometry.num_vertices = 3
geometry.has_vertices = True
geometry.has_normals = True
geometry.bs_data_flags.has_uv = True
for field in ("vertices", "normals", "uv_sets"):
    geometry.reset_field(field)   # sizes each array to num_vertices, all zero
# Corners (0,0), (1,0), (0,1): used as-is for the UVs, and scaled down to 0.01 units for the positions
for vertex, uv, (x, y) in zip(geometry.vertices, geometry.uv_sets[0], ((0, 0), (1, 0), (0, 1))):
    vertex.x, vertex.y = x * 0.01, y * 0.01
    uv.u, uv.v = x, y
for normal in geometry.normals:
    normal.z = 1.0   # facing up
geometry.set_triangles([(0, 1, 2)])
geometry.update_center_radius()   # bounding sphere from the vertices

helper = Nif.NiTriShape(data)
helper.name = "MojaveShimmerStrengthControl"
helper.flags = 0x8000F   # bit 0 = hidden, same as the wireframe
helper.add_property(texturing)
helper.add_property(unlit)
helper.data = geometry

# Right after the cylinder, where it's always been in the block list
children = root.get_children()
children.insert(children.index(cylinder) + 1, helper)
root.set_children(children)

with open(nif_path, "wb") as stream:
    data.write(stream)
print(f"[MojaveShimmer] Added the strength trick to {nif_path}")
