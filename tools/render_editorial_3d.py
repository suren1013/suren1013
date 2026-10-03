"""Original dossier monogram and conceptual heat-sink study, Blender 4.2."""
import bpy
import math
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
def mat(name,color,metal=0,texture=False):
    m=bpy.data.materials.new(name);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Metallic'].default_value=metal
    p.inputs['Roughness'].default_value=0.62 if texture else 0.35
    if texture:
        n=m.node_tree.nodes.new('ShaderNodeTexNoise');n.inputs['Scale'].default_value=70
        b=m.node_tree.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=0.25;b.inputs['Distance'].default_value=0.07
        m.node_tree.links.new(n.outputs['Fac'],b.inputs['Height']);m.node_tree.links.new(b.outputs['Normal'],p.inputs['Normal'])
    return m
def box(name,loc,size,material):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.scale=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(material)
    b=o.modifiers.new('Machined edges','BEVEL');b.width=0.035;b.segments=3
    o.modifiers.new('Surface normals','WEIGHTED_NORMAL')
    return o
def light(loc,color,energy,size,target):
    bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object
    o.data.energy=energy;o.data.color=color;o.data.shape='DISK';o.data.size=size
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
def setup(target,position,scale):
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    s=bpy.context.scene;s.render.engine='BLENDER_EEVEE_NEXT';s.eevee.taa_render_samples=96
    s.render.resolution_x=1100;s.render.resolution_y=950;s.render.resolution_percentage=100
    s.world.color=(0.013,0.014,0.015)
    s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast'
    s.view_settings.exposure=-1.0
    bpy.ops.object.camera_add(location=position);o=bpy.context.object
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    o.data.type='ORTHO';o.data.ortho_scale=scale;s.camera=o
    return s
def render(s,name):
    s.render.image_settings.file_format='PNG';s.render.filepath=str(ROOT/'assets'/name)
    bpy.ops.render.render(write_still=True)

s=setup((0,0,0.9),(5,-10,5.8),7.5)
concrete=mat('Cast stone',(0.32,0.31,0.29),texture=True)
graphite=mat('Architecture',(0.045,0.047,0.052),texture=True)
red=mat('Vermilion',(0.5,0.015,0.008))
box('Plinth',(0,0,-0.33),(7,5,0.6),graphite)
curve=bpy.data.curves.new('Original SR monogram','FONT');curve.body='SR'
curve.font=bpy.data.fonts.load('C:/Windows/Fonts/arialbd.ttf');curve.size=3.1
curve.extrude=0.22;curve.bevel_depth=0.025;curve.bevel_resolution=3
o=bpy.data.objects.new('Concrete initials',curve);bpy.context.collection.objects.link(o)
o.location=(-2.1,0.05,0);o.rotation_euler=(math.pi/2,0,0);o.data.materials.append(concrete)
box('Red registration slab',(2.6,0.5,1.4),(0.1,1.8,3.4),red)
box('Suspended block',(-2.3,1.7,3.2),(0.65,0.65,0.65),concrete)
light((-3,-5,7),(0.86,0.89,1),1800,6,(0,0,1))
light((4,2,4),(1,0.035,0.015),1900,4,(0,0,1))
render(s,'dossier-emblem.png')

s=setup((0,0,0.7),(9,-12,8),10.2)
metal=mat('Brushed aluminium',(0.36,0.39,0.42),0.7)
graphite=mat('Charcoal floor',(0.028,0.03,0.034),texture=True)
red=mat('Conceptual heat-source marker',(0.45,0.02,0.012),0.3)
box('Architectural floor',(0,0,-0.8),(50,50,0.4),graphite)
box('Base plate',(0,0,0),(6,4,0.45),metal)
box('Conceptual source',(0,0,-0.35),(2.8,2.2,0.25),red)
for i in range(13): box('Fin %02d'%i,(-2.7+i*0.45,0,1.1),(0.13,4,1.7),metal)
light((-4,-3,8),(0.78,0.83,1),2600,7,(0,0,1))
light((5,4,6),(1,0.09,0.04),2000,5,(0,0,1))
light((1,-7,3),(1,0.9,0.8),700,4,(0,0,0))
render(s,'heat-sink-concept.png')
