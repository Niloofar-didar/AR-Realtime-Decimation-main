import bpy
#import Mathutils
import bmesh
import sys
import time
import argparse
import os
import shutil
from bpy import context
USE_FILTER_FACES = True

# blender -b -P Vol_Area.py --  --inm objects_name.txt 

#reads from an input of address for all objects and writes name of object, volume and area in size_data.txt

########################### functions
def bmesh_from_object_final(ob):
    import bmesh
    matrix = ob.matrix_world
    me = ob.to_mesh(context.scene, apply_modifiers=True, settings='PREVIEW')
    me.transform(matrix)
    bm = bmesh.new()
    bm.from_mesh(me)
    bpy.data.meshes.remove(me)
    if USE_FILTER_FACES:
        faces_remove = [f for f in bm.faces if not is_face_skip(f)]
        for f in faces_remove:
            bm.faces.remove(f)
    return (bm, matrix.is_negative)

def volume_and_area_from_object(ob):
    bm, is_negative = bmesh_from_object_final(ob)
    volume = bm.calc_volume(signed=True)
    area = sum(f.calc_area() for f in bm.faces)
    bm.free()
    if is_negative:
        volume = -volume
    #area= area * 10000
    #volume= volume * 1000000
    return volume, area

#self.report({'INFO'}, "Volume: %.2f" % volume)
def is_face_skip(f):
    """Ignore faces that pass this test!"""
    return f.hide is False


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

main_address="/Server/input/"

with open(infile, "r") as inp, open("size_data.txt", "w") as out:

 for line in inp:

   inp= line[:-1]
   namee=inp[:-4]
    

   print (str(inp) + "   "+str(namee))
   print('\n Clearing blender scene (default garbage...)')
   # deselect all
   bpy.ops.object.select_all(action='DESELECT')
   for o in bpy.data.objects:
            if o.type == 'MESH':
                bpy.data.objects.remove(o)

   print('\n Beginning the process of import & export using Blender Python API ...')

   bpy.ops.import_scene.obj(filepath=main_address+ namee+ "/"+inp)

   print('\n Obj file imported successfully ...')
   bpy.context.scene.objects.active = bpy.context.selected_objects[0]
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
   ctx['selected_editable_bases'] = [scene.object_bases[ob.name] for ob in obs]

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
    volume_single, area_single = volume_and_area_from_object(ob)
    volume += volume_single
    area += area_single
    #print("From %d object(s) polygon" + str(len(ob.data.polygons))+ " obj name: "+ str(ob))
    object_count += 1
   volume = abs(volume)

   tris= len(ob.data.polygons)

   print("From %d object(s) polygon " + str(len(ob.data.polygons))+ " obj name: "+ str(ob))
   #token = inp.split("obj/")
   #token1=token[1].split(".obj")
   #model=token1[0]

  # to write


   #Now checking for textures in the folder of the input mesh.... (plz change if needed)
   allfilelist= os.listdir(main_address+ namee)
   #print(allfilelist)

   for Afile in allfilelist[:]: 
     if not(Afile.endswith(".png") or Afile.endswith(".PNG") or Afile.endswith(".jpg") or Afile.endswith(".JPG") or Afile.endswith(".bmp") or Afile.endswith(".BMP")):
        allfilelist.remove(Afile)


   #print(allfilelist)
   texture="Yes"
   if len(allfilelist)==0 :
      print('\n List is empty. No texture file')
      texture="No"
   else:
     print('\n Found the LIST of images in PNG and JPEG (textures): ')
     print(allfilelist)




   message=" %.4f %.4f %4d %s" % (volume, area, tris, texture)
   #out.write(model+message+"\n")
   out.write(namee+message+"\n")




