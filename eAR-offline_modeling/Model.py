

# This is to get all the required information for each object degradation model including the distance and degradation error for four decimation ratios , you need to check to have all the required inputs in a correct directory


### Code Provider: *N*

import os
import bpy
import bmesh
import sys
import time
import argparse
import mathutils
import math
import shutil


def get_args():
  parser = argparse.ArgumentParser()

  #Critical View finder:(Screenshot phase) gets obj and simp level, then put obj at closest dist #with original and simplified quality, at 6 diff fov- screen shots , out put in 12 scresshot per #each obj-> then feed to IQ2 to found critical view
  #blender -b -P Model.py -- --infile Objects/CriticInp.txt
  #blender-2.79-linux-glibc219-x86_64/blender -b -P test.py
  
  _, all_arguments = parser.parse_known_args()
  double_dash_index = all_arguments.index('--')
  script_args = all_arguments[double_dash_index + 1: ]
 
# add parser rules

  parser.add_argument('-fil', '--infile', help="Third Object")
  parsed_script_args, _ = parser.parse_known_args(script_args)
  return parsed_script_args
 
args = get_args()

infile=str(args.infile)
print(infile)

with open(infile, "r") as inp:
    
    count= inp.readline()
    

#bpy.data.objects['Camera'].rotation_euler= mathutils.Vector((1.1087, -0.0,0.8150688))
bpy.data.cameras.values()[0].lens=25
bpy.data.cameras['Camera'].lens=25

angles=4

with open(infile, "r") as inp, open("Objects/Screenshots/compare.txt", "w") as out:
    
    count= inp.readline()
    finalcount= float(count)*angles *2
    out.write(str(finalcount)+ "\n")

    for line in inp:

        #bpy.data.objects['Camera'].location = mathutils.Vector((7.35889 , -6.92579 , 4.95831 )) #11.243 from object
        input_model,Objname,Dratio = map(str,line.split())
        
        #Dist=float(TDis) # it is preffered distance
        
        
	# deselect all
        bpy.ops.object.select_all(action='DESELECT')
	# selection
        
        
        for o in bpy.data.objects:
            if o.type == 'MESH':
                bpy.data.objects.remove(o)
           


        print('\n Beginning the process of import using Blender Python API ...\n')
        bpy.ops.import_scene.obj(filepath=input_model)
        print('\n Obj file imported successfully ...')
        scene = bpy.context.scene
        obs=[]
        #should be comment-for inf just
        for o in bpy.data.objects:
            if o.type == 'MESH':
                xx=o.location.x
                yy=o.location.y
                zz=o.location.z
                curobj=o

                i=1
                camx =bpy.data.objects['Camera'].location.x
                camy =bpy.data.objects['Camera'].location.y
                camz =bpy.data.objects['Camera'].location.z

                dx = camx - xx
                dy = camy - yy
                dz = camz - zz
                distance= math.sqrt(pow(dx, 2) + pow(dy, 2) + pow(dz, 2))
                print ("Distance "+str(i)+": "+str(distance))
                print('\n Ending Distance...')
                obs.append(o)
         #should be comment-         

        

         

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




#nil



        bpy.data.objects["Camera"].rotation_euler = mathutils.Vector((1.110029, 0.0, 0.8150688)) 
        curobj.select=True # select object
        
        bpy.ops.view3d.camera_to_view_selected()
        bpy.data.objects["Lamp"].location= bpy.data.objects["Camera"].location
        camloc=bpy.data.objects["Camera"].location
        print("cam location is "+ str(camloc))
        curobj.select=False # select object

       
 
        

#nil    

	#start rotating object, simplification  and screenshot
        bpy.context.scene.render.image_settings.file_format='BMP'
        output_dir="Objects/Screenshots/"
        output_file_format="bmp"
        rotation_steps = 5

        degree=0.872665
        for o in bpy.data.objects:
            if o.type == 'MESH':

              decimateRatio = float(1)
              for step in range(1, 3):

                 print('\n Beginning the process of Decimation using Blender Python API ...')
                 modifierName='DecimateMod'
                 modifier = o.modifiers.new(modifierName,'DECIMATE')
                 modifier.ratio = decimateRatio
                 print("dec ratio is "+ str(decimateRatio))
                 modifier.use_collapse_triangulate = True
                 bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifierName)

              
                 for step in range(1, rotation_steps):
                     
                     
                     o.rotation_euler=mathutils.Vector((1.5708, -0.0, degree))

                     # deselect all
                     bpy.ops.object.select_all(action='DESELECT')
	             # selection
        
                     curobj.select=True # select object
                     bpy.ops.view3d.camera_to_view_selected()
                     

                     xx=o.location.x
                     yy=o.location.y
                     zz=o.location.z
                     obj=o

                     objloc=o.location
                     print("current obj is "+ str(obj)+" and obj location is "+ str(objloc))

                     i+=1
                     camx =bpy.data.objects['Camera'].location.x
                     camy =bpy.data.objects['Camera'].location.y
                     camz =bpy.data.objects['Camera'].location.z
                   
                     dx = camx - xx
                     dy = camy - yy
                     dz = camz - zz
                     distance= math.sqrt(pow(dx, 2) + pow(dy, 2) + pow(dz, 2))
                     print ("Distance "+str(i)+": "+str(distance))
                     print('\n Ending Distance...')             
                   
                     bpy.context.scene.render.filepath = output_dir + (Objname +str(step))+ "d"+ str(round(distance))+ "r"+str(decimateRatio)
    
                     bpy.ops.render.render(write_still = True)
                     

                     out.write(output_dir + (Objname +str(step))+ "d"+ str(round(distance))+"r"+str(decimateRatio)+ ".bmp"+"\n")
                     degree+=1.5708
                      


               
                
                 decimateRatio = float(Dratio)



#end of screenshot

angles=4

# start comparing ranks of all views ( start of IQA2.py code)

#opens in3 to read all images for compare, open out to write all results, open IQAout for just one result from ubuntu
with open("Objects/Screenshots/compare.txt", "r") as inp, open("Objects/Screenshots/outIQA.txt", "w") as out:
  


  numinp=float(inp.readline())
  
  lines = inp.readlines()
  print(lines[0])
  
  i=0
  index=0
  print(numinp)
  
  
  a = []
  b = []
  name=[]
 
  while i<numinp:
     for j in range(0, angles):
        a.append (lines[i+j])
        b.append (lines[i+j+angles])
        temp1=a[index]
        temp1=temp1[:-1] #trims one char at the  end to remove \n char
     
        temp2=b[index]
        temp2=temp2[:-1]
    
   
        # print(str(temp1) + " "+ str(temp2)+ " "+str(a))
      
        path="wine gmsd.exe"
        end=" > \"Objects/Screenshots/IQAout.txt\" "
        #final = "wine gmsd.exe Objects/Screenshots/Andy1d1r1.0.bmp Objects/Screenshots/Andy1d1r0.5.bmp > IQAout.txt"  
	
        final ="wine gmsd.exe %s %s > Objects/Screenshots/IQAout.txt" %(temp1, temp2)
        #each iqa for one comparison to be saved on iqaout and then are written to the out file 
        # print(final)
        os.system(final)
        with open("Objects/Screenshots/IQAout.txt", "r") as iqa:
	  #out.write(str(j+1)+" "+iqa.readline())
          out.write(iqa.readline())
        index+=1

     objname=lines[i]
     objname=objname[20:-12] #omit file address too have just name of object
     address="Objects/obj/%s.obj " %objname
     
     print(address)
     name.append (address)
     i+=(angles*2)
    
print("start checking critical view")        
with open("Objects/Screenshots/outIQA.txt", "r") as inpp, open("Objects/Screenshots/cresult.txt", "w") as outt:       
   i2=0
   j2=0
   lines2 = inpp.readlines()
   while i2<numinp/2:
       maxim= max(lines2[i2:i2+angles])
       maxdex= lines2.index(maxim)
       fmaxdex=maxdex%angles + 1

       minim= min(lines2[i2:i2+angles])
       mindex= lines2.index(minim)
       fmindex=mindex%angles + 1
       print("maximum is "+ str(maxim)+ " "+str(fmaxdex)+"\n")
       print("minimum is "+ str(minim)+ " "+str(fmindex))

       i2+=angles
     
       outt.write(str(fmaxdex) + " " + name[j2]+"\n")
       #outt.write(str(fmindex) + " " + name[j2]+"\n")
       j2+=1


# end of IQ2 and start of distance.py to decimate model and put them at diff distances:

camlens =bpy.data.cameras.values()[0].lens=25
bpy.data.cameras['Camera'].lens=25



#opens in3 to read all images for compare, open out to write all results, open
#IQAout for just one result from ubuntu

lmp=bpy.data.objects["Lamp"]
bpy.data.objects.remove(lmp)


#add new lamp

scene = bpy.context.scene

# Create new lamp datablock
lamp_data = bpy.data.lamps.new(name="Lamp2", type='HEMI')

# Create new object with our lamp datablock
lamp_object = bpy.data.objects.new(name="Lamp2", object_data=lamp_data)

# Link lamp object to the scene so it'll appear in this scene
scene.objects.link(lamp_object)

camera= bpy.context.scene.camera.data
camera.clip_end=1000
camera.clip_start=0.001


#Starting object z-height on camera sensror calculation:

#



camlens =bpy.data.cameras.values()[0].lens=25

with open("Objects/Screenshots/cresult.txt", "r") as inp, open("Objects/finalObj/model.txt", "w") as out,open("Objects/finalObj/virdistance.txt", "w") as vdist, open("Objects/finalObj/camerapos.txt", "w") as campos:
    #no_of_cases = str(inp.readline())
    #print(no_of_cases)
    for line in inp:

       
       # deselect all
        bpy.ops.object.select_all(action='DESELECT')
	# selection
        
        
        #input_model,Objname,Dratio,TDis = map(str,line.split())
        angle_num,input_model = map(str,line.split())
        angle = int( angle_num)
        objname= input_model
        objname=objname[12:-4] #omit file address too have just name of object

        print("angle is " + str(angle))
        scene = bpy.context.scene
        obs=[]
## flush environment before importing new object
        for o in bpy.data.objects:
            if o.type == 'MESH':
                bpy.data.objects.remove(o)
       ##

        print('\n Beginning the process of import using Blender Python API ...\n')
        bpy.ops.import_scene.obj(filepath=input_model)
        print('\n Obj file imported successfully ...')

        for o in bpy.data.objects:
            if o.type == 'MESH':
                  obs.append(o)


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



        for o in bpy.data.objects:
            if o.type == 'MESH':
                xx=o.location.x
                yy=o.location.y
                zz=o.location.z
                curobj=o
                

       
     #nil
        bpy.data.objects['Camera'].location = mathutils.Vector((7.35889 , -6.92579 , 4.95831 )) #11.243 from object
        
        bpy.ops.object.select_all(action='DESELECT')
	# selection

        # this is min cam distance: 
        curobj.select=True 
        # select object
        curobj.location=mathutils.Vector((0.0, -0.0 , 0.0 )) #11.243 from object
        

        if angle==1:
                    degree=mathutils.Vector((1.5708, -0.0, 0.872665))  

        elif angle==2:
                    degree= mathutils.Vector((1.5708, -0.0, 0.872665+1.5708)) 


        elif angle==3:
                    degree= mathutils.Vector((1.5708, -0.0, 0.872665+(2*1.5708)))


        elif angle==4:
                    degree= mathutils.Vector((1.5708, -0.0, 0.872665+(3*1.5708)))

          
        elif angle==5:
                    degree=mathutils.Vector((2.61799, -3.50811, 3.735)) 

        elif angle==6:
                    degree=mathutils.Vector((4.60767, -2.00713, 5.63741)) 

        curobj.rotation_euler=degree 
       
        bpy.data.objects["Camera"].rotation_euler = mathutils.Vector((1.110029, 0.0, 0.8150688)) 

        bpy.ops.view3d.camera_to_view_selected()

       
#
        bpy.context.scene.render.image_settings.file_format='BMP'
        output_dir="Objects/finalObj/"
        

        bpy.context.scene.render.filepath = output_dir +objname

        bpy.ops.render.render(write_still = True)


#Nill2
        camloc=bpy.data.objects["Camera"].location
        camlocx=str(camloc.x)
        camlocy=str(camloc.y)
        camlocz=str(camloc.z)
        
        print("cam location is "+ str(camloc))
        curobj.select=False # select object

#n


 # in order to find the fit view of object, closets distance from camera to obj that fits object, then we use the distance as a reference to calculate all dimension for the preffered distance

      
	

#start computing distance
        print('\n Starting Distance Computing...')
        camx =bpy.data.objects['Camera'].location.x
        camy =bpy.data.objects['Camera'].location.y
        camz =bpy.data.objects['Camera'].location.z


        obj= curobj
        xx=obj.location.x
        yy=obj.location.y
        zz=obj.location.z

        dx = camx - xx
        dy = camy - yy
        dz = camz - zz
        distance= math.sqrt(pow(dx, 2) + pow(dy, 2) + pow(dz, 2))
        inc_factor=distance #*0.5# increament distacne by this
        # so the factor to multiply cam location by each time is incremental + old_distance/ old_distance:  e.g, old-d =1 , inc = 0.5 => factor = 1 + 0.5 / 1= 1.5=> 1.5 * 1= 1.5

# next sould be 2 so factor= 1.5 + 0.5 / 1.5 =1.33 => 1.33 * old 1.5 = 2

        print ("distance is "+ str(distance))
        print('\n Ending Distance...')
        
# MAx Distance: 

        Height= curobj.dimensions.z
        #print("dz object Dimension is "+ str(curobj.dimensions.z))
        Vz= (camlens* Height)/distance
        Vx=(camlens* curobj.dimensions.x)/distance
        Vy=(camlens* curobj.dimensions.y)/distance
        
        fac1= Vx/(0.758)
        fac2= Vy/(0.758)
        fac3=Vz/(0.758)
        DFactor= (fac1+fac2+fac3)/3
        print(" Facts are " + str(fac1) +"," + str(fac2)+"," + str(fac3))
        print(" Dfactor is " + str(DFactor))
        #change camera location based on the distance in input


        #print( "Max distance will be "+str(distance * DFactor )+" and actual Distance was  :"+ str(distance))

        Maxdistance= math.sqrt(pow(DFactor*dx, 2) + pow(DFactor*dy, 2) + pow(DFactor*dz, 2))

        #print( "Max distance by computation will be "+str(newdistance))
 
        



#after importing we start simplification
       #start rotating object, simplification  and screenshot

        rotation_steps = 5
        vir_distance=False
        #degree=0.872665

        old_ratio=new_ratio=1
        #bpy.data.objects["Lamp"].location= bpy.data.objects["Camera"].location
        decimateRatio = float(1)
        #for o in bpy.data.objects:
           # if o.type == 'MESH':
        dis_indx=0
        campos_flag=False
        campos.write( str(objname)+ "\n")
        for step in range(1, 6): # 5 simplification levels screenshots
        #for step in range(1, 2):   
   
               bpy.data.objects["Camera"].location.x= float(camlocx)
               bpy.data.objects["Camera"].location.y= float(camlocy)
               bpy.data.objects["Camera"].location.z= float(camlocz)
               first_time=False
               distance=0
               
         
               while  distance<Maxdistance :
               #while  distance<5 :
                 bpy.data.objects["Lamp2"].location= bpy.data.objects["Camera"].location
        
                 #curobj.rotation_euler=mathutils.Vector((1.5708, -0.0, 0.872665))
                 #i+=1

                 dx = bpy.data.objects['Camera'].location.x - 0
                 dy = bpy.data.objects['Camera'].location.y - 0
                 dz = bpy.data.objects['Camera'].location.z - 0

                 distance= math.sqrt(pow(dx, 2) + pow(dy, 2) + pow(dz, 2))
                 #print ("Distance "+str(i)+": "+str(distance))
                 #print('\n Ending Distance...')

                 Vz= (camlens* Height)/distance
                 if vir_distance==False:
                   vdist.write( str(round(distance,2))+" " + str(Vz)+"\n")

                 if first_time==False: 
                     
                     #camera's view
                     curobj.select=True
                     bpy.ops.view3d.camera_to_view_selected()
                     first_time=True

                 #Nil temprary
                 curobj.rotation_euler=degree  
                 bpy.context.scene.render.filepath = output_dir +objname+ "deg"+ str(angle)+"d"+ str(round(distance,2))+ "r"+str(round(new_ratio,2))
                 bpy.ops.render.render(write_still = True)
                 out.write(output_dir +objname+ "deg"+ str(angle)+"d"+ str(round(distance,2))+ "r"+str(round(new_ratio,2))+ ".bmp"+"\n")
                 

                 if(campos_flag==False):
                    
                     campos.write( str(round(distance,2))+" "+ str(dx) + " " + str(dy) + " "+ str(dz)+"\n")
       
                 
                  #changinf camera location
                 mul_fact= (inc_factor+ distance) / distance

                 bpy.data.objects['Camera'].location.x *= mul_fact
                 bpy.data.objects['Camera'].location.y *=mul_fact
                 bpy.data.objects['Camera'].location.z*=mul_fact
                 

               campos_flag=True
                # print( "changed dim x, y, z is "+ str(bpy.data.objects['Camera'].location.x)+ str(bpy.data.objects['Camera'].location.y)+ str(bpy.data.objects['Camera'].location.z ))
               vir_distance=True  
               old_ratio=new_ratio # 1 as old ratio
              # print("screen shot was taken and dec ratio was "+ str(old_ratio))
              # print('\n Beginning the process of Decimation using Blender Python API ...')
               bpy.context.scene.objects.active = o
              # print("before decimation object {} has {} verts, {} edges, {} polys".format(curobj.name, len(curobj.data.vertices), len(curobj.data.edges), len(curobj.data.polygons)))
               new_ratio=old_ratio- float(0.20) # 0.8 as new ratio
               new_ratio= round(new_ratio,2)
               decimateRatio = new_ratio/old_ratio 
               modifierName='DecimateMod'
               modifier = curobj.modifiers.new(modifierName,'DECIMATE')
               modifier.ratio = decimateRatio
               
               modifier.use_collapse_triangulate = True
               bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifierName)
   
               #print("After decimation object {} has {} verts, {} edges, {} polys".format(curobj.name, len(curobj.data.vertices), len(curobj.data.edges), len(curobj.data.polygons)))

               
# end of distance.py



# start IQA3.py to rank model
          
with open("Objects/finalObj/model.txt", "r") as inp, open("Objects/finalObj/FinalIQA.txt", "w") as out:
  


  #numinp=float(inp.readline())
  
  lines = inp.readlines()
  
  i=0
  index=0
  
  token=lines[0]
  token=token[35:-5]
  ind=0
  token3=token2=token #token2 is always fixed to first object value/ ratio num
  object_index=ind


  
  for step in range(1, int(count)+1):


    first=False # first time writing the distance

    if object_index>= len(lines):
      break
 
    token=lines[object_index]
# fr finalObj/.. we start from index 18 but for finalObj2 it has one mre word so start from 19



    token=token[17:-5]
    #token=token[19:-5]
    token = token.split("deg");
    tok = token[1].split("r");
    token2=token3= tok[1]


    while token2==token3:

     token=lines[i]
     print (str(i))
     #token=token[19:-5]
     token=token[17:-5]
     # 19 instead of 18 is for times when we have finalobj2 as destination which changes object addreses in one word of "2" instead of nothing
     token = token.split("deg");
     tok = token[1].split("r");
     token3= tok[1]
     #print (str(token3))

     i+=1 # final i shows number of distances for each object- first one is 21
    
  
    
    for j in range(object_index,i-1): 

      if object_index> len(lines):
        break
      b=[]
      a = lines[j]
      a=a[:-1]
      # it is for 4 diff simplification level 
      temp2=lines[1*(i-1-object_index)+j]
      temp2=temp2[:-1]
      b.append (temp2)
      temp2=lines[2*(i-1-object_index)+j]
      temp2=temp2[:-1]
      b.append (temp2)
      temp2=lines[3*(i-1-object_index)+j]
      temp2=temp2[:-1]
      b.append (temp2)
      temp2=lines[4*(i-1-object_index)+j]
      temp2=temp2[:-1]
      b.append (temp2)
      #print (str(a) + "\n")
      #print (str(b) +"\n")
      
      step=0
      while(step!=4):

         final ="wine gmsd.exe %s %s > Objects/finalObj/Final.txt" %(a, b[step])
         os.system(final)
         with open("Objects/finalObj/Final.txt", "r") as iqa:
          out.write(iqa.readline())

         step+=1
     
    object_index=(object_index+ ((i-1)-object_index)*5)
    i=object_index  
    #print i
    out.write("\n") 



# end of model and start of seprating results based on distance as well as degradation error



with open("Objects/finalObj/FinalIQA.txt", "r") as inp5, open("Objects/finalObj/Degradation_Error.txt", "w") as out5:

# here we will write down deg error from 0.8 for obj 1 to 0.2 by space then we'll have another object starting from 0.8 to 0.2---> using the corresponding data is possibe by knowing num of objects and num of distances  ===> we get num of objects by the first line in distances.txt and num of distances per obj by lines in distances file before an endl


  #numinp=float(inp.readline())
  
  lines = inp5.readlines()
  # in each four lines starting from first line, first is for 0.8, next is 0.6, ,04, 0.2... and it repeats so if index of lines array %4==0 it is 0.8 , we have  space line between diff objects


  index= lines.index('\n')  

  
  while (lines.count('\n')> 0 ): 
      
    tmplines=lines[:index] #separates each obj inf from 0.8 to 0.2     
    print(index)
    print("new object")
    print(tmplines)

    ind=0
    j=0;
    counter= len(tmplines)/4 ; # holds number of error value in each ratio
    print(str(counter))
    while j<4: # holds number of ratios

     ind=j  # in inner for we get error value per each ratio and we go to next ratio
     for ii in range(0,int(counter)): 
       out5.write(tmplines[ind])
       ind= ind+4;
     out5.write("\n")
     j=j+1; 
     
    lines = lines[index+1: len(lines)] 
    index= lines.index('\n')
    tmplines=lines[:index]  
   



# end of fetching deg-error (IQA3.py) results and start to fetch distances  (data.py)
with open("Objects/finalObj/model.txt", "r") as inp, open("Objects/finalObj/Distances.txt", "w") as out:
  

  out.write(str(count) +"\n")
  #numinp=float(inp.readline())
  
  lines = inp.readlines()
  
  i=0
  j=0
  written=0
  #while i<len(lines):
  obj_index=0
  for step in range(1,int(count)+1): 
  #num of objects (if you have 3 just put (1,4)

   dis1=0

   first =False
   while i<len(lines):
     token=lines[i]
     #print i
     
     token=token[17:-7]
     token = token.split("deg");
     
     temp2=token[1]
     temp2 = temp2.split("d");
     temp=temp2[1]
     temp3=temp.split("r")
     temp=temp3[0]
     #print (temp)
     
     if (dis1== temp):
        print (" before i is "+str( i)+ "and objindex is "+str( obj_index) )
        i=(obj_index+ ((i)-obj_index)*5) # to the num of decima
        obj_index=i # 1- index=15 , 2th: 15 + (18-15)*5
        print (" after i is "+str( i)+ "and objindex is "+str( obj_index) )
        first= False
        name=( token[0])
        print (name +"\n")
        out.write(name+ "\n")
        out.write("\n")
        #written+=1
        #break

     else:
      out.write(temp+ "\n")
      #dis1=temp
      
      if (first==False):
       dis1=temp
       first=True
       


      print (str(temp)+ " " +str(dis1) )
        
      i+=1 # final i shows number of distances for each object- first one is 21

     
### Code Provider: *N

