
import os
import bpy
import bmesh
import sys
import time
import argparse
import mathutils
import math
import shutil
from mathutils import Quaternion

import random
import statistics
import math 
from math import sqrt

#import pandas as pd 
import numpy as np  
import array
import csv
import array as arr 
#import matplotlib.pyplot as plt  
#import seaborn as seabornInstance 

'''
this code is for our user study survey to quantify user percieved quality
takes the degradation model and find the best qualitu for each distance having maximum deg constraint

 blender -b -P test.py


'''




def QualitySelection_reverse(ind,d11): # this is to find candidate qualities based on factor * max_deg 
# factors are 0.2 . 0.4 and 0.6
     
    i=ind
    gamma=float(gamm[i])
    a= float(alpha[i])
    b=float(beta[i])
    c1=float(c[i])
    
    
  
    c3=c1- ((d11** gamma)* max_deg[i] * 0.6)
    c2= c1- ((d11** gamma)* max_deg[i] * 0.4)
    c1=c1-((d11** gamma)* max_deg[i] * 0.2) # ax2+bx+c= (d^gamma) * max_deg


    inp1=[1.0,1.0,1.0]
    inp2=[1.0,1.0,1.0]
 
    #print("first equation")
    r1,r2=delta(a,b,c1,c[i],d11,gamma,max_deg[i] * 0.2 )
    r1= float(round(r1,2))
    r2=float(round(r2,2))
    
    #inp1.append(r1)
   # inp2.append(r2)
    inp1[0]=r1
    inp2[0]=r2
    #print("second equation")
    
    r1,r2= delta(a,b,c2,c[i],d11,gamma, max_deg[i] * 0.4)
    r1= float(round(r1,2))
    r2=float(round(r2,2))
    inp1[1]=r1
    inp2[1]=r2

    r1,r2= delta(a,b,c3,c[i],d11,gamma, max_deg[i] * 0.6)
    r1= float(round(r1,2))
    r2=float(round(r2,2))
    inp1[2]=r1
    inp2[2]=r2
   
    
    
    
    #need fixing !!!
    sel_inp=0 # selects amon inp1 or inp2
    final_inp = array.array('f')
    final_inp=[1.0,1.0,1.0]
  
   
    for i in range (0,3):
        
        if(inp1[i]==0 and inp2[i]==0):
            final_inp[i]=1.0
        
        elif( inp2[i]==0 or inp2[i]==1)  :
            final_inp[i]=inp1[i]
        else:
            if( inp1[i]==0 or inp1[i]==1): 
              final_inp[i]=inp2[i]
            else:
                 final_inp[i]=min (inp2[i], inp1[i])
         
    return final_inp
     
     
def delta(a,b,c,c_real,d,gm, max_d):
  #("Quadratic function : (a * x^2) + b*x + c=0")
  r=0.0
  r = (b**2 - 4*a*c)

  if r > 0:
    num_roots = 2
    x1 = (((-b) + sqrt(r))/(2*a))     
    x2 = (((-b) - sqrt(r))/(2*a))
    #print("There are 2 roots: %f and %f" % (x1, x2))
    if(0.1<x1<1.0 and 0.1<x2<1.0):
      return x1,x2
    if (0.1<x1<1) :
      x=checkerror(a, b, c_real, d, gm, max_d) 
      #x=1
      return x1,x
    if (0.1<x2<1) :
      x=checkerror(a, b, c_real, d, gm, max_d)
      #x=1
      return x,x2
    else:
      x=checkerror(a, b, c_real, d, gm, max_d)
      #x=1
      return x,x
  
    
  elif r == 0:
    num_roots = 1
    x = (-b) / 2*a
    #print("There is one root: ", x)
    return x,0
  else:
    num_roots = 0
    #print("No roots, discriminant < 0.")
    x=checkerror(a, b, c_real, d, gm, max_d)
    #x=1
    return x,x
    #0 is delta1 here      
     


def checkerror(a,b,creal,d,gamma, max_d):
    
    
    r1=0.1
    error=max_d
    for i in range (1,18):
        
     error = ((a* (r1**2)) + b*r1 + creal) / (d**gamma)
     if(error<max_d):
       return r1
     r1+=0.05
     #r2=0.8
     #error2 = ((a* (r2**2)) + b*r2 + creal) / (d**gamma)

    return 0



alpha=[]
beta=[]
#min_dis=[] # minimum distance between user and each obj -> let it be similar for all objects
c=[]
gamm=[]
max_deg=[]
tris=[]
o_name=[]
mindis=[]
filesize=[]

     
     
#dataset = pd.read_csv("degmodel_file.csv")



with open('degmodel_file.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    line_count = 0
    
    
    for row in csv_reader:
      temp1=str(row)
      temp= (temp1.split(","))

     
      if(temp[0][2:-1]!= "alpha"):
       alpha.append(float(temp[0][2:-1])) # remove extra unused signs as [ and '
       beta.append(float(temp[1][2:-1]))
       c.append(float(temp[2][2:-1]))
       gamm.append(float(temp[3][2:-1]))
       max_deg.append(float(temp[4][2:-1]))
       tris.append(float(temp[5][2:-1]))
       o_name.append(temp[6][2:-1])
       mindis.append(float(temp[7][2:-1]))
       filesize.append(temp[8][2:-1])



 # stores worse case decimation which is from 1 to 0.9 as eg,, from 1 to 0.2 is 0.2 * (t of 0.9)
#max_deg_error=0.01 # should be a list for all objs indeed/ this is for simplification 
#gpu = 3e-5 t + 45
i=0

obj_count=len(alpha)


distance = [2,4,6]

objects_quality=[] 
with open('qualities_reversal.txt', mode='w',newline='') as qual:
    
 for i in range(0, obj_count):
  
  name=str(o_name[i])
  
  qual.write(str(name)+ "\n")

 
  #
  temp=[]
  j=0
  factor=[]
  for elm in distance:
   temp.append(QualitySelection_reverse(i, elm))
   temp3=(temp[j])
   factor.append(elm)
   #temp3=temp2.split(",")
   
   qual.write(str(elm)+" " + str(temp3[0])+" "+ str(temp3[1]) +" "+str(temp3[2])+" " +"\n")
   j+=1
  
  objects_quality.append(temp)
  






#using qualities_reversal as input for puting objects at 3 candidate distances with candidate ratios


# this code is for user study and quantifying max degradation eerror


#blender-2.79-linux-glibc219-x86_64/blender -b -P test.py
#blender -b -P Model.py -- --infile Objects/CriticInp.txt
# end of IQ2 and start of distance.py to decimate model and put them at diff distances:



angles=4


# end of IQ2 and start of distance.py to decimate model and put them at diff distances:

camlens =bpy.data.cameras.values()[0].lens=25
bpy.data.cameras['Camera'].lens=25



#opens in3 to read all images for compare, open out to write all results, open
#IQAout for just one result from ubuntu

lmp=bpy.data.objects["Lamp"]
bpy.data.objects.remove(lmp)


#add new lamp

scene = bpy.context.scene
scene.world.horizon_color = (0.721,0.7211,0.721)

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




#dis, vx, vy,vz for camera pos

#2.0	1.025350332	-0.986288071	1.408393145
				
#6	3.326379061	-3.090707779	3.882926702
			
#4.0	2.050700903	-1.97257638	2.816786051

camlens =bpy.data.cameras.values()[0].lens=25


with open("Objects/Screenshots/cresult.txt", "r") as inp, open("Objects/finalObj/qualities.txt", "w") as out, open("qualities_reversal.txt", "r") as qual, open("Objects/finalObj/camerapos.txt", "w") as campos:
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

       
#Nill2
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

        #nil    


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
        #for step in range(1, 6): # 5 simplification levels screenshots

        camx_pos=[1.025350332, 3.326379061, 2.050700903]
        camy_pos=[-0.986288071, -3.090707779, -1.97257638]
        camz_pos=[1.408393145, 3.882926702, 2.816786051]

        dis=[2,4,6]

        obj_ind=o_name.index(objname)
        print(str(obj_ind)+" " + str(objname))


        #



        
        #  (0, 0, 1) i blue
        # black

        print("campos=" + str(camx_pos[0]) + " " + str(camy_pos[1]))

        fact=1
        first_time=True
        for step in range (0,4): ## decimation two times
  
            bpy.data.objects["Camera"].location.x= float(camlocx)
            bpy.data.objects["Camera"].location.y= float(camlocy)
            bpy.data.objects["Camera"].location.z= float(camlocz)

            new_ratio=1

            #if referesh_dis==True: 
                     
                     #camera's view
            curobj.select=True
            bpy.ops.view3d.camera_to_view_selected()
            

            for indx in range(0, 3):   
               # distance loop for factors of 0.2,04 and 0.6 mac deg error


               dx = bpy.data.objects['Camera'].location.x - 0
               dy = bpy.data.objects['Camera'].location.y - 0
               dz = bpy.data.objects['Camera'].location.z - 0

               distance= math.sqrt(pow(dx, 2) + pow(dy, 2) + pow(dz, 2))
               

   
               #changinf camera location
               mul_fact= dis[indx] / distance
               if(mul_fact>1) :

                 bpy.data.objects['Camera'].location.x *= mul_fact
                 bpy.data.objects['Camera'].location.y *=mul_fact
                 bpy.data.objects['Camera'].location.z*=mul_fact

            
               if (first_time==False) :
                   temp=objects_quality[obj_ind]

                   print (temp)
                   temp3=(temp[indx])
                   print(temp3[step-1]) # for first factor 0.2 max deg error
           
# step-1 = 0 is factor of 0.2, if =1, is factor of 0.4 else it is factor of 0.6

                   fact=factor[step-1]/10

                   old_ratio=new_ratio # 1 as old ratio
                   bpy.context.scene.objects.active = o
            
                   #new_ratio=
                   new_ratio= temp3[step-1]

                   curobj.select=True
                   #print("before decimation object {} has {} verts, {} edges, {} polys".format(curobj.name, len(curobj.data.vertices), len(curobj.data.edges), len(curobj.data.polygons)))

                   new_ratio= round(new_ratio,2)
                   decimateRatio = new_ratio/old_ratio 
                   modifierName='DecimateMod'
                   modifier = curobj.modifiers.new(modifierName,'DECIMATE')
                   modifier.ratio = decimateRatio
               
                   modifier.use_collapse_triangulate = True
                   bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifierName)

               else:
                     fact=1 #means original object


                   #print(" dec ratio of "+ str(decimateRatio)+ " After decimation object {} has {} verts, {} edges, {} polys".format(curobj.name, len(curobj.data.vertices), len(curobj.data.edges), len(curobj.data.polygons)))


               
               
               bpy.data.objects["Lamp2"].location= bpy.data.objects["Camera"].location
        
               dx = bpy.data.objects['Camera'].location.x - 0
               dy = bpy.data.objects['Camera'].location.y - 0
               dz = bpy.data.objects['Camera'].location.z - 0

               distance= math.sqrt(pow(dx, 2) + pow(dy, 2) + pow(dz, 2))
                 #print ("Distance "+str(i)+": "+str(distance))
           

               
               curobj.rotation_euler=degree  
               bpy.context.scene.render.filepath = output_dir +objname+ "fact"+ str(fact)+"d"+ str(round(distance,2))+ "r"+str(round(new_ratio,2))
               bpy.ops.render.render(write_still = True)
               out.write(output_dir +objname+ "fact"+ str(fact)+"d"+ str(round(distance,2))+ "r"+str(round(new_ratio,2))+ ".bmp"+"\n")


            first_time=False # outside the distance loop


            for o in bpy.data.objects:
              if o.type == 'MESH':
                #bpy.ops.object.delete(o)
                bpy.data.objects.remove(o)



            scene = bpy.context.scene
            obs=[]


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
	
            curobj.select=True 
            # select object
            curobj.location=mathutils.Vector((0.0, -0.0 , 0.0 )) #11.243 from object
 
            curobj.rotation_euler=degree 
       
            bpy.data.objects["Camera"].rotation_euler = mathutils.Vector((1.110029, 0.0, 0.8150688)) 

            bpy.ops.view3d.camera_to_view_selected()








               #if(campos_flag==False):
                    
                     #campos.write( str(round(distance,2))+" "+ str(dx) + " " + str(dy) + " "+ str(dz)+"\n")

               #campos_flag=True
               #end of distance.py

            

