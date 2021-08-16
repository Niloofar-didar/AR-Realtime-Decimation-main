import bpy
#import Mathutils
import bmesh
import sys
import time
import argparse
from bpy import context
USE_FILTER_FACES = True

# AndroidStudioProjects/helloAR_Master_Research_Eric/Server/blender-2.80-linux-glibc217-x86_64/blender -b -P glb.py --  --inm objects.txt 

#reads from an input of address for all objects and exports glb file

########################### functions

def get_args():
  parser = argparse.ArgumentParser()
 
  # get all script args
  _, all_arguments = parser.parse_known_args()
  double_dash_index = all_arguments.index('--')
  script_args = all_arguments[double_dash_index + 1: ]
 
  # add parser rules
 # add parser rules
  #parser.add_argument('-hei', '--height', help="Ratio of reduction, Example: 0.5 mean half number of faces ")
  parser.add_argument('-in', '--inm', help="Original Model")
  
  parsed_script_args, _ = parser.parse_known_args(script_args)
  return parsed_script_args

 
args = get_args()

#height = float(args.height)
#print(height)

infile = str(args.inm)


with open(infile, "r") as inp:

 for line in inp:

   inp= line[:-1]
   print (str(inp))
   print('\n Clearing blender scene (default garbage...)')
   # deselect all
   bpy.ops.object.select_all(action='DESELECT')
   for o in bpy.data.objects:
            if o.type == 'MESH':
                bpy.data.objects.remove(o)

   print('\n Beginning the process of import & export using Blender Python API ...')
   bpy.ops.import_scene.obj(filepath=inp)
   print('\n Obj file imported successfully ...')
   bpy.context.view_layer.objects.active  = bpy.context.selected_objects[0]
   print("poly is  "+str(len(bpy.context.object.data.polygons)))

   ### just imported obj

   scene = bpy.context.scene

   obs = []
   for ob in scene.objects:
    # whatever objects you want to join...
     if ob.type == 'MESH':
         obs.append(ob)

   ctx = bpy.context.copy()

   # one of the objects to join
   ctx['active_object'] = obs[0]

   ctx['selected_objects'] = obs
   # In Blender 2.8x this needs to be the following instead:
   #ctx['selected_editable_objects'] = obs

   # We need the scene bases as well for joining.
   # Remove this line in Blender >= 2.80!
   #ctx['selected_editable_bases'] = [scene.object_bases[ob.name] for ob in obs]

   bpy.ops.object.join(ctx)



   volume = 0.0
   area = 0.0
   object_count = 0
   modifierName='TRIANGULATE'
   for ob in context.selected_objects:
    if ob.type != 'MESH':
        continue

    #un-comment this to apply triangulation for new objects:

    #modifier = ob.modifiers.new(modifierName,'TRIANGULATE')
    #bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifierName)
    #bpy.ops.export_scene.obj(filepath=inp)
   
    #print("From %d object(s) polygon" + str(len(ob.data.polygons))+ " obj name: "+ str(ob))
    

   #token = inp.split("obj/")
   #token1=token[1].split(".obj")
   #model=token1[0]
   
   # to write
   bpy.ops.export_scene.gltf(filepath= inp[:-4])
   #bpy.ops.export_scene.gltf(filepath= output_model)
   print('\nProcess of exporting glb Finished ...')
   

