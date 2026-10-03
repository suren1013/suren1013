"""Original 3D profile artwork. Blender 4.2: --background --python tools/render_control.py"""
import bpy, math, random
from pathlib import Path
from mathutils import Vector
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build' / 'frames'
OUT.mkdir(parents=True, exist_ok=True)
random.seed(17)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.eevee.taa_render_samples = 32
scene.render.resolution_x = 1000
scene.render.resolution_y = 440
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.fps = 18
scene.world.color = (0.025, 0.025, 0.025)
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Medium High Contrast'
scene.view_settings.exposure = -2.0
def material(name, color, texture=False, metallic=0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    n = m.node_tree.nodes
    bs = n.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (*color, 1)
    bs.inputs['Roughness'].default_value = 0.78
    bs.inputs['Metallic'].default_value = metallic
    if texture:
        noise = n.new('ShaderNodeTexNoise')
        noise.inputs['Scale'].default_value = 85
        noise.inputs['Detail'].default_value = 3
        bump = n.new('ShaderNodeBump')
        bump.inputs['Strength'].default_value = 0.27
        bump.inputs['Distance'].default_value = 0.06
        m.node_tree.links.new(noise.outputs['Fac'], bump.inputs['Height'])
        m.node_tree.links.new(bump.outputs['Normal'], bs.inputs['Normal'])
    return m
concrete = material('Cast concrete', (0.12, 0.115, 0.105), True)
dark = material('Graphite', (0.045, 0.047, 0.052), True, 0.12)
red = material('Vermilion', (0.5, 0.006, 0.003))
ivory = material('Ivory', (0.78, 0.77, 0.70))
def emission(name, color):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes
    n.clear()
    e = n.new('ShaderNodeEmission')
    e.inputs['Color'].default_value = (*color, 1)
    e.inputs['Strength'].default_value = 3
    output = n.new('ShaderNodeOutputMaterial')
    m.node_tree.links.new(e.outputs[0], output.inputs['Surface'])
    return m
ivory = emission('Typesetting / unlit ivory', (0.82, 0.8, 0.75))
panel_mat = emission('Editorial panel', (0.006, 0.007, 0.008))
def box(name, loc, size, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    b = o.modifiers.new('Physical edges', 'BEVEL')
    b.width = 0.025
    b.segments = 2
    o.modifiers.new('Corner normals', 'WEIGHTED_NORMAL')
    return o
box('Floor', (0, 0, -2.8), (60, 60, 0.3), concrete)
box('Rear monolith', (0, 5, 2), (60, 0.6, 25), concrete)
box('Crimson aperture', (3.2, 4.55, 2), (0.12, 0.16, 15), red)
for x in (-12, -8, 9, 13):
    box('Architecture', (x, 2, 1), (1.4, 3, 14), concrete)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.8, location=(2.6, 0, 0.6))
hedron = bpy.context.object
hedron.name = 'HEDRON / suspended icosahedron'
hedron.data.materials.append(dark)
b = hedron.modifiers.new('Cut edges', 'BEVEL')
b.width = 0.015
b.segments = 1
blocks = []
for i in range(14):
    a = i * math.tau / 14
    loc = (2.6 + math.cos(a) * random.uniform(2.5, 4.4), random.uniform(-0.4, 1.8), 0.6 + math.sin(a) * random.uniform(2, 3.4))
    s = random.uniform(0.25, 0.7)
    o = box('Suspended concrete %02d' % i, loc, (s, s * 1.3, s), concrete)
    o.rotation_euler = (random.random(), random.random(), random.random())
    blocks.append((o, o.location.copy(), o.rotation_euler.copy(), a))
def area(name, loc, color, energy, size):
    bpy.ops.object.light_add(type='AREA', location=loc)
    o = bpy.context.object
    o.name = name
    o.data.color = color
    o.data.energy = energy
    o.data.shape = 'DISK'
    o.data.size = size
    o.rotation_euler = (Vector((2, 0, 0)) - o.location).to_track_quat('-Z', 'Y').to_euler()
area('Architectural key', (0, -5, 7), (0.8, 0.83, 1), 1800, 7)
area('Red intrusion', (6, 2.5, 3), (1, 0.01, 0.005), 2700, 5)
area('Edge light', (1, 3, 6), (1, 0.8, 0.64), 2200, 4)
bpy.ops.object.camera_add(location=(0, -19, 4.4))
cam = bpy.context.object
cam.rotation_euler = (Vector((0, 0, 0.5)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
cam.data.type = 'ORTHO'
cam.data.ortho_scale = 16
scene.camera = cam
panel = box('Editorial field', (0, 0, 0), (7.15, 7.1, 0.01), panel_mat)
panel.parent = cam
panel.location = (-4.43, 0, -10.05)
font = bpy.data.fonts.load('C:/Windows/Fonts/arialbd.ttf')
def label(text, x, y, size):
    curve = bpy.data.curves.new('Typeset', 'FONT')
    curve.body = text
    curve.font = font
    curve.size = size
    curve.space_character = 1.15
    o = bpy.data.objects.new(text, curve)
    bpy.context.collection.objects.link(o)
    o.parent = cam
    o.location = (x, y, -10)
    o.data.materials.append(ivory)
label('RESEARCH / IN PROGRESS', -7.1, 2.65, 0.19)
label('ORDER', -7.1, 0.65, 0.94)
label('FROM', -7.1, -0.25, 0.94)
label('COMPLEXITY.', -7.1, -1.15, 0.75)
label('THERMAL SYSTEMS  /  CFD  /  SOFTWARE', -7.1, -2.25, 0.16)
label('01   /   COMPUTATIONAL STUDIES', -7.1, -2.75, 0.15)
scene.frame_start = 1
scene.frame_end = 72
for f in range(1, 73):
    t = math.tau * (f - 1) / 72
    hedron.rotation_euler = (0.22 + 0.12 * math.sin(t), t, 0.17)
    hedron.location.z = 0.6 + 0.18 * math.sin(t)
    for o, base, rot, phase in blocks:
        o.location = base + Vector((0.10 * math.sin(t + phase), 0, 0.25 * math.sin(t + phase)))
        o.rotation_euler = (rot.x + 0.14 * math.sin(t + phase), rot.y + 0.18 * math.cos(t + phase), rot.z)
    scene.frame_set(f)
    scene.render.filepath = str(OUT / ('%04d.png' % f))
    bpy.ops.render.render(write_still=True)
print('Rendered 72 seamless frames to', OUT)
