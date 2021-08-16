import bpy
import bmesh
import sys
import time
import argparse

# blender -b -P Resize.py -- --height 0.8  --inm Objects/Bed.obj --outm oBed2.obj



def get_args():
  parser = argparse.ArgumentParser()
 
  # get all script args
  _, all_arguments = parser.parse_known_args()
  double_dash_index = all_arguments.index('--')
  script_args = all_arguments[double_dash_index + 1: ]
 
  # add parser rules
 # add parser rules
  parser.add_argument('-hei', '--height', help="Final Height Dimension")
  parser.add_argument('-in', '--inm', help="Original Model")
  parser.add_argument('-out', '--outm', help="Rescaled output file")
  parsed_script_args, _ = parser.parse_known_args(script_args)
  return parsed_script_args

 
args = get_args()

height = float(args.height)
print(height)

input_model = str(args.inm)
print(input_model)

output_model = str(args.outm)
print(output_model)

print('\n Clearing blender scene (default garbage...)')
# deselect all
bpy.ops.object.select_all(action='DESELECT')

print('\n Beginning the process of import & export using Blender Python API ...')
bpy.ops.import_scene.obj(filepath=input_model)
print('\n Obj file imported successfully ...')


### just imported obj

print('\n Starting Resize...')
print('\n Z Dimension of the object is')


for o in bpy.data.objects:
    if o.type == 'MESH':
        z=o.dimensions.z
 	



#x= bpy.data.objects[0].dimensions.x
#y=bpy.data.objects[0].dimensions.y
#z=bpy.data.objects[0].dimensions.z

# Resize the object

newscale=1
print(z)

if z != 0 :
  newscale= height/z

bpy.ops.transform.resize(value=(newscale,newscale,newscale))

print('\n new scale is',newscale ,'\n')

#bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

bpy.ops.export_scene.obj(filepath=output_model)

print('\n Ending Resize...')











