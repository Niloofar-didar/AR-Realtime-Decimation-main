
import os
import sys
import time
import argparse

import math
import shutil


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
this code is for finding the potential for saving energy- let's say we define 3 distances 2,4,6 meter and for each distance we find the lowest quality for each obj having maximum deg constraint
then, we find the sum of all tris and use the gpu utilization model by a= 4.1786369783353056e-05
b=44.25345492837267

gives two files, one quality potential and 2, gpu, tris and distance inf in gpu_result.txt

blender -b -P test.py
'''

def QualitySelection_reverse(ind,d11): # this is to find candidate qualities based on factor * max_deg 
# factors are 0.2 . 0.4 and 0.6
     
    i=ind
    gamma=float(gamm[i])
    a= float(alpha[i])
    b=float(beta[i])
    c1=float(c[i])
    

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
    
    #need fixing !!!
    sel_inp=0 # selects amon inp1 or inp2
    final_inp = array.array('f')
    final_inp=[1.0,1.0,1.0]
  
   
    for i in range (0,1):
        
        if(inp1[i]==0 and inp2[i]==0):
            final_inp[i]=1.0
        
        elif( inp2[i]==0 or inp2[i]==1)  :
            final_inp[i]=inp1[i]
        else:
            if( inp1[i]==0 or inp1[i]==1): 
              final_inp[i]=inp2[i]
            else:
                 final_inp[i]=min (inp2[i], inp1[i])
         
    return final_inp[0]
     
     
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



i=0

obj_count=len(alpha)


distance = [2,4,6,8]

objects_quality=[] 
total_tris1=[0,0,0,0] # in three distances (2,4,6,8) before optimization

total_tris2=[0,0,0,0] # in three distances (2,4,6,8) after optimization


with open('qualities_reversal_potential.txt', mode='w',newline='') as qual:
    
 for i in range(0, obj_count):
  
  name=str(o_name[i])
  
  qual.write(str(name)+ "\n")

 

  temp=[]
  j=0
  factor=[]
  for elm in distance:
   temp.append(QualitySelection_reverse(i, elm))
   temp3=(temp[j])
   factor.append(elm)

  
#The scenario has 3count of these objects plus a bike and plane---> total-onj *3 + tris of the plane and bike of the objects

   if(name=="plant" or name=="bike" or name=="table" or name=="hammer"  or name== "plane" or name=="BigCabin" ):

     total_tris2[j]+= 3*(tris[i] * temp3)
     total_tris1[j]+= 3* (tris[i] * 1)

     if(name=='bike'):
        total_tris2[j]+= (tris[i] * temp3)
        total_tris1[j]+= (tris[i] * 1)
     elif(name=='plane'):
        total_tris2[j]+= (tris[i] * temp3)
        total_tris1[j]+= (tris[i] * 1)
   
   qual.write(str(elm)+" " + str(temp3)+"\n")
   j+=1



print(total_tris2)
print(total_tris1)

a_gpu= 4.1786369783353056e-05
b_gpu=44.25345492837267
gpu1=[0,0,0,0]
gpu2=[0,0,0,0]



print(gpu1)
print(gpu2)


with open('gpu_result.txt', mode='w',newline='') as qual:
  for i in range(0,4):

    gpu1[i] = (a_gpu* total_tris1[i] ) + b_gpu
    gpu2[i] = (a_gpu* total_tris2[i] ) + b_gpu
    

  for i in range(0,4):
    qual.write(str(distance[i])+" " + str(total_tris1[i])+" " + str(gpu1[i])+ "\n")


  qual.write("\n")
  qual.write("\n")

  for i in range(0,4):
    qual.write(str(distance[i])+" " + str(total_tris2[i])+" "+ str(gpu2[i])+"\n")



