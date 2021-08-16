#!/usr/bin/python3
import bpy
import sys
import time
import argparse
import os

'''
This is to read object names and find the tris num and file size in bit to tris_filesize.txt, storing to another filr named tris.txt
'''
#blender -b -P tris.py -- --inm objects.txt
 
def get_args():
  parser = argparse.ArgumentParser()
 
  # get all script args
  _, all_arguments = parser.parse_known_args()
  double_dash_index = all_arguments.index('--')
  script_args = all_arguments[double_dash_index + 1: ]
 
  # add parser rules
  parser.add_argument('-in', '--inm', help="input adress of objects")
 
  parsed_script_args, _ = parser.parse_known_args(script_args)
  return parsed_script_args
 


def tris(input_model):

 with open(input_model, "r") as inp, open("tris_fileseize.txt", "w") as out:
    
    for line in inp:
# Clear Blender scene
       for o in bpy.data.objects:
         if o.type == 'MESH':
           o.select = True
         else:
           o.select = False
         
# call the operator once
       bpy.ops.object.delete()    

       input_model = str(line[:-1])
      
       bpy.ops.import_scene.obj(filepath=input_model)
     
       glbfile= str(input_model[:-3] + "glb")
       print("glb is" + glbfile)
       file_stats = os.stat(glbfile)
       print(f'File Size in Bytes is {file_stats.st_size}')
       #print(f'File Size in MegaBytes is {file_stats.st_size / (1024 * 1024)}')

       size=  (file_stats.st_size) # in byte
       bitsize= size * 8  

       Mgabyte=size/ (1024 * 1024)
       print( str(bitsize) + " bitsize")

       print('\n Obj file imported successfully ...')
       
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
  
       bpy.ops.object.join(ctx)

       

       modifierName='TRIANGULATE'
       for obj in bpy.data.objects:
            if obj.type == 'MESH':
               obj.select=True
               bpy.context.scene.objects.active = obj
               objname= input_model[12:-4]
               #print(" real obj name: "+objname)
               #print(" name: {}".format(obj.name))
               #print("{} has {} verts, {} edges, {} polys".format(obj.name, len(obj.data.vertices), len(obj.data.edges), len(obj.data.polygons)))
               #modifier = obj.modifiers.new(modifierName,'TRIANGULATE')
               
               #bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifierName)
               #print("{} has {} verts, {} edges, {} polys after TRIANGULATE ".format(obj.name, len(obj.data.vertices), len(obj.data.edges), len(obj.data.polygons)))
               poly= str(len(obj.data.polygons))
              

               out.write(objname + " "+str( len(obj.data.polygons)) + " " + str(Mgabyte)+ "\n")

    return poly   

# we have main here
args = get_args()

input_model = str(args.inm)

fpoly= tris(input_model)
print('\n final poly num ...' + str(fpoly))               
