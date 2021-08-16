# -*- coding: utf-8 -*-
"""

gets the general GPU usage model considering th emodel of each scenario and relative graphs

Created on Fri Aug 28 06:35:45 2020
finds the gpu model parameters
@author: N
"""
import matplotlib.gridspec as gridspec
import matplotlib.image as img
import matplotlib.pyplot as plt
import random
import numpy as np
import networkx as nx
from itertools import *
import pandas as pd  
import numpy as np  
import csv
import array as arr 
import pylab
import math 
import matplotlib.pyplot as plt  
import seaborn as seabornInstance 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.metrics import mean_squared_error, r2_score
dataset = pd.read_csv("\\OCT\\GPU.csv")

fig = plt.figure()

print("HIII")

intercept_b=43.60365902313669

a_array=[]
b_array=[ ]# to store all coeefficients for gpu model]
NRMSE_array=[]
plt.rcParams.update({'font.size': 14})


# =============================================================================
# dataset.plot(x='Tris16', y='GPU16', style='o')  
# plt.title('GPU vs Tris')  
# plt.xlabel('Tris')  
# plt.ylabel('GPU Percentage')
# plt.savefig('foo.png')  
# plt.show()
# =============================================================================

markers = ['>', 'x','.','^','h','+' ,'h']
#markers = ['>', '+', '.', 'o', 'v', 'x', 'X', '|','^','<','s','p','|','^','<','>', '+', '.', 'o', 'v', 'x', 'X', '|','^','<','s','p','|','^','<','s','p','*','h' ,'*','h','H','1',',','H','1']
'''colors=[    'b', 'g',  'r', 'c', 'm', 'y', 'orange','violet','navy','blueviolet','teal','lightcoral' ,'gold','olive','deepskyblue', 'pink', 'grey',  'firebrick','deeppink',
        'lawngreen','slategrey', 'goldenrod' ,'coral', 'rosybrown', 'darkcyan',  
        'steelblue','dimgrey', 'darkgreen', 'fuchsia', 'peachpuff' ,'tan','darkolivegreen'   ,'sandybrown'    ,'pink','yellow'     ]
'''
colors=[ 'gold' , 'b', 'g', 'red', 'darkorange', 'darkorchid'
        #'orange','navy','lightcoral' 
        ]

dataset2=[]
dataset2 = pd.read_csv("\\OCT\\GPU.csv",nrows=1)


with open("\\OCT\\GPU.csv") as f:
    reader = csv.reader(f)
    i = (next(reader))
    
column=len(i)    

'''
anotation=['andy','andy','andy','andy','plane','plane','andy','andy','andy','andy','andy','plane','plane','andy',
'andy','andy','andy','andy','plane','plane','andy','andy','andy','andy','andy','plane','plane','andy','andy','andy',
'andy','andy','plane','plane','andy','andy','andy','andy','andy','plane']
'''
anotation=[ 'ATV', 'Cabin', 'Desk' ,'apricot','plant','washingmachine',
'andy','drawer','shoe','table', 'splane', 'roomtable', 'plant','jean_obj','new_five_andy'
,'hammer','football_ball_OBJ', 'bike', 'airplane' ,'GarbageFinal', 'hammer', 'shoe'
,'washingmachine', 'plane', 'apricot', 'andy']




X=[]
y=[]
f = plt.figure() 
stored_ind=[]
labels=[]
#fig = plt.figure(figsize=(6.5,4.5))
for k in range(1, int(column/5)+1, 1):

    tris=[]
    objname=(dataset['name'+str(k)].values.reshape(-1,1))        
    tris= dataset['Tris'+str(k)]
    i=0

    
    
        
    if ( objname[0]=="mixed4-adding"   or objname[0]=="mixed5-adding"
           or objname[0]=="mixed8-adding" 
     
         or objname[0]=="mixed5-decimating"  or objname[0]=="mixed4-decimating"
         or objname[0]=="mixed8-decimating"  
         #or objname[0]=="apricot-decimating"    or objname[0]=="statue-decimating"  or objname[0]=="ATV-adding"       or objname[0]=="smallandy-adding" 
         ):
        
        
        value = random.randint(0, 5)
        while(stored_ind.count(value)): #avoid duplicated elm
           value = random.randint(0, 5)
   
        stored_ind.append(value)
 
# =============================================================================
# =============================================================================
#     if(objname[0]!="ATV-adding" and  objname[0]!="smallcabin-adding"and  objname[0]!="smallandy-adding" and  objname[0]!="drawer-adding"
#        and  objname[0]!="bigandy-adding"and  objname[0]!="bigcabin-adding" and  objname[0]!="giantplant-adding" 
#       # and  objname[0]!="mixed1-adding"and  objname[0]!="mixed2-adding"   and  objname[0]!="mixed3-adding"
#      #  and  objname[0]!="bigplane-expp1" 
#      #  and  objname[0]!="bigplant-adding"and  objname[0]!="airplane-adding"   and  objname[0]!="stone-adding" and objname[0]!="stone-decimating"
#       and   objname[0]!="roomtable-adding" and objname[0]!="roomtable-decimating"and  objname[0]!="coca3-adding" and objname[0]!="bigplane-decimating"and  objname[0]!="bigplane-adding" 
#        and objname[0]!="smallplane-decimating"and  objname[0]!="smallplane-adding" and  objname[0]!="statue1-adding" 
#    and  objname[0]!="coca-decimating"and  objname[0]!="coca-adding"   and  objname[0]!="statue-decimating"and  objname[0]!="statue-adding" 
#    and  objname[0]!="apricot-decimating"and  objname[0]!="apricot-adding" 
#   # and  objname[0]!="andyplane-adding"
#   #and  objname[0]!="mixed3-adding" 
#        # and  objname[0]!="mixed2-adding" and  objname[0]!="mixed4-adding"  and  objname[0]!="mixed5-adding" and  objname[0]!="mixed8-adding" 
#         # and  objname[0]!="mixed4-decimating"  and  objname[0]!="mixed5-decimating"  and  objname[0]!="mixed8-decimating"
#         
#    ):
# =============================================================================
        

        
        #if ( objname[0]=="andyplane-adding"):
        if ( objname[0]=="mixed1-adding"):   
            tris_tmp = (dataset['Tris'+str(k)])
            gpu_tmp= (dataset['GPU'+str(k)])
            for i in range (0, len(gpu_tmp)):
                if(math.isnan(gpu_tmp[i])== False  ):
                  if(i>0 and  tris_tmp[i]-tris_tmp[i-1] >100000):   
                    #plt.annotate(anotation[i],(float( tris_tmp[i]),float( gpu_tmp[i] )))
                    plt.scatter(float( tris_tmp[i]),float( gpu_tmp[i] ),marker='o', color='r')
                 
                  else:
                      plt.scatter(float( tris_tmp[i]),float( gpu_tmp[i] ),marker='o', color='r')
                 
                else:
                    break
        else:
          plt.plot((dataset['Tris'+str(k)]), (dataset['GPU'+str(k)]),marker= markers[value],color=colors[value],linestyle='') 
       

        if (objname[0]=="mixed4-adding" ):
            objname[0]="Add 1"
            
        elif (objname[0]=="mixed5-adding" ):
            objname[0]="Add 2"
            
        elif (objname[0]=="mixed8-adding" ):
            objname[0]="Add 3"
                        
        elif (objname[0]=="mixed4-decimating" ):
            objname[0]="Decimate 1"
            
        elif (objname[0]=="mixed5-decimating" ):
            objname[0]="Decimate 2"
        elif (objname[0]=="mixed8-decimating" ):
            objname[0]="Decimate 3"
            
        obj=str(objname[0][0])     
        labels.append(obj)
        
    
  
      
#plt.legend(["Cabine_exp1","Roomtable_exp1","Plane_exp2", "Mixed objects_ exp2" ])      
ax = plt.gca()      
#ax.legend(handles, labels)
#plt.legend(labels, loc="upper center", bbox_to_anchor=(1.26,1 ), ncol=3, fontsize=9)
plt.legend(labels, loc="upper center", bbox_to_anchor=(0.32,1 ), ncol=2,fontsize=11)

#ax.set_yscale('log')
ax.set_xscale('log')      
plt.xlabel('Total Number of Triangles on Screen', fontsize=14)  
plt.ylabel('GPU Utilization (%)', fontsize=14)      
plt.tight_layout()
plt.rcParams['font.size'] = '18'
plt.rcParams['lines.markersize'] = 10
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["axes.labelweight"] = "bold"
plt.savefig("GPU_plot.pdf", dpi=300, bbox_inches = 'tight')


plt.show()
plt.close()

total_images = 4
testimg3= img.imread('\\OCT\\andy-pic.bmp')
testimg2= img.imread('\\OCT\\bike-pic.bmp')
testimg4= img.imread('\\OCT\ATV-pic.bmp')
testimg1= img.imread('\\OCT\CocacolaFinal-pic.bmp')
testimage=[testimg1,testimg2,testimg3,testimg4]

images = {'Image'+str(i): testimage[i] for i in range(total_images)}

#plt.figure(1,constrained_layout=True,figsize=(2,2))

#for i in range (0,4):



''' # find the GPU model'''


for i in range(1, int(column/5)+1, 1):

    #if(i==30):
      #i+=1
   X= ( dataset['Tris'+str(i)].values.reshape(-1,1))
   y=(dataset['GPU'+str(i)].values.reshape(-1,1))
   area_=(dataset['Area'+str(i)].values.reshape(-1,1))
   vol=(dataset['Volume'+str(i)].values.reshape(-1,1))
   name=(dataset['name'+str(i)].values.reshape(-1,1))

   #Nill
   # you neeed to consider the min and max threshold for gpu model
    #if(X[0]>42000): # to check the threshold for linear model
    

   if ( name[0]=="Add 1"   or name[0]=="Add 2"
            or name[0]=="Add 3" 
      
          or name[0]=="Decimate 1"  or name[0]=="Decimate 2"
          or name[0]=="Decimate 3"  
          #or objname[0]=="apricot-decimating"    or objname[0]=="statue-decimating"  or objname[0]=="ATV-adding"       or objname[0]=="smallandy-adding" 
          ):
    
    # =============================================================================
    
    '''u need to uncomment this for getting a genatal gpu model'''    
    # =============================================================================
    #    if(name[0]!="bigandy-adding" and name[0]!= "bigcabin-adding"
    #         and  name[0]!="drawer-adding" and name[0] != "ATV-adding"  ):
    # =============================================================================
    
    # =============================================================================
    #    if(name[0]!="bigandy-adding" and name[0]!= "bigcabin-adding"
    #         and  name[0]!="drawer-adding" and name[0] != "ATV-adding"  ):   
    # =============================================================================

       
       
    area_vol=[] # their multiplication to test for equation
    area_vol3=[] 
    area_vol2=[] 
    area_vol4=[] 
    area=[]
    volume=[]
    area2=[]
    volume2=[]
    total_tris=[]
    c=[]
    gpu0=[]


#
    j=1
    while(j<=len(y)):
    
        if((pd.isnull(vol[j-1]))) :
            break
     
        
        elif ( X[j-1]>42000):
            
            volume2.append(float(vol[j-1]))
            area2.append(float(area_[j-1]))
            #area.append(float(area_[j-1]**(1/2)))
            #volume.append(float(vol[j-1])**(1/3))
            total_tris.append(float(X[j-1]))
            gpu0.append(float(y[j-1]))
            area_vol.append( float( (float(area_[j-1])**(1/2)) *X[j-1]))
            area_vol2.append(float((  float(area_[j-1]**(1/2))  + float(vol[j-1])**(1/3) ) *X[j-1]))
            area_vol3.append( float(  float(area_[j-1]**(1/2))   *  float(vol[j-1])**(1/3) *X[j-1]) )
            area_vol4.append( float( X[j-1]) ) 
            #area_vol3.append( float( ((volume[j-1]**(1/6))) *X[j-1]) )
            #area_vol4.append( float( X[j-1])) 
            c.append(1)
            j=j+1
       
        else:
            j=j+1

    row_count =len(total_tris)
    
    if(total_tris[len(total_tris)-1]  < 1000000):
        print (name[0] + " " + str( total_tris[len(total_tris)-1]))
    

#a area + b vol + ctris +d
    Z3 = [np.array(area2),np.array(volume2),np.array(total_tris),np.array(c)  ]
    Za3= np.array(Z3).transpose()[:]


# a vol*area + btris + c
    Z4 = [np.array(area_vol4),np.array(c)  ]
    Za4= np.array(Z4).transpose()[:]
    
     #A*TRIS*VOL + B
    Z2 = [np.array(area_vol),np.array(c)  ]
    Za2= np.array(Z2).transpose()[:]


    GPU_real = np.array(gpu0)

    #print(GPU)  

    reg2 = LinearRegression(fit_intercept=False).fit(Za2, GPU_real)
    coeffs2=reg2.coef_.tolist()
    coeffs2.append(reg2.intercept_)
    #print("second")
    #print(coeffs2)
    #cof2 = 
    a2=coeffs2[0]
    b2 = coeffs2[1]
    
   

    reg3 = LinearRegression(fit_intercept=False).fit(Za3, GPU_real)
    coeffs3=reg3.coef_.tolist()
    coeffs3.append(reg3.intercept_)
    #print("third")
    #print(coeffs3)
    #cof3 = coeffs3[0]
    a3=coeffs3[0]
   #print(a3)
    b3 = coeffs3[1]
    c3=coeffs3[2]
    d3=coeffs3[3]
    #why it is a problem???
    
    reg4 = LinearRegression(fit_intercept=False).fit(Za4, GPU_real)
    coeffs4=reg4.coef_.tolist()
    coeffs4.append(reg4.intercept_)
     #print("main forth")
    print(coeffs4)

    #coeffs4[0]
    a4=coeffs4[0]
    b4 = coeffs4[1]
    
    
    
    a_array.append(a4)
    b_array.append(b4)

    model_values2 = []
    model_values3 = []
    model_values4 = []
    total_models=[]
#mse=[]
    for i in range(0, row_count, 1):
        
       
   
         # = a1 * area_vol[i] + b1 * total_tris[i] + c1
         #model_values1.append(result1)
       
    
         result2 = a2 * area_vol2[i]+ b2
         model_values2.append(result2)
         #a area + b vol + ctris +d
         result3 = a3 * area2[i] + b3 *volume2[i]+ c3* total_tris[i] + d3
         #result3 = a3 * area_vol3[i] + b3
         model_values3.append(result3)
     
         result4 = a4 *area_vol4 [i] + b4 
         model_values4.append(result4)
    
#total_models.append(model_values1) 
    total_models.append(model_values2) 
    total_models.append(model_values3) 
    total_models.append(model_values4) 

#print(total_models[0])
    perc_err=[]
    nrmse=[]
    for i in range(0, len(total_models), 1):
        rmse= mean_squared_error(GPU_real, total_models[i], squared=False )
        #mse2= mean_squared_error(GPU, total_models[i] )
        #rmse2= np.sqrt(mse2)
        #rms = mean_squared_error(y_actual, y_predicted, squared=False)
        
        # rmse = np.sqrt(mse)
        nrmse.append(rmse/(100-intercept_b)) # normalized rmse
        perc_err.append(np.mean(np.abs((GPU_real - total_models[i]) / GPU_real)) * 100)
        #print("percentage error for model "+ str(i+1)+ " is " + str(perc_err[i]))
        #print('NRMSE (no intercept): for model    + {} '.format(nrmse[i]))
  
    
    file2 = open("GPU_reg2.txt","a+") 
    file2.write(str(name[0])+ " " +str(a2 )+ " "+str( b2)  + " " + str(perc_err[0] )+ " "+str(nrmse[0])+ "\n" )
    file2.close()
    print("eq2: "+str(name[0])+ " " +str(a2 )+ " "+str( b2) + " "+str(nrmse[0])+ "\n" )
    
    file3 = open("GPU_reg3.txt","a+") 
#file.write(str(name[0])+ " " +str(a4 )+ " "+str( b4) + " " + str(c4) + " " + str(perc_err[3] )+ " "+str(nrmse[3])+ "\n" )
    file3.write(str(name[0])+ " " +str(a3 )+ " "+str( b3)+" " +str(c3 )+ " "+str( d3) + " " + str(perc_err[1] )+ " "+str(nrmse[1])+ "\n" )
    file3.close()
    print("eq3: "+str(name[0])+ " " +str(a3 )+ " "+str( b3) +" " +str(c3 )+ " "+str( d3) +  " "+str(nrmse[1])+ "\n" )
 
#coeffs = [ round(elem, 4) for elem in coeffs[1] ]
    file4 = open("GPU_reg4.txt","a+") 
    file4.write(str(name[0])+ " " +str(a4 )+ " "+str( b4)  + " " + str(perc_err[2] )+ " "+str(nrmse[2])+ "\n" )
    file4.close()
    print("eq4: "+str(name[0])+ " " +str(a4 )+ " "+str( b4) + " "+str(nrmse[2])+ "\n" )
    NRMSE_array.append(nrmse[2])

average_a = sum(a_array) / len(a_array)
average_b = sum(b_array) /len(b_array)
average_NRMSE= sum(NRMSE_array)/ len(NRMSE_array)
'''this is the mean NRMSE for dedicated models while average-a and b are the 
parameters for the general model that would be used in GPU_perc general model and error code'''


print(average_a)
print (average_b)
print(average_NRMSE) 
print ("NRMSE foe each dedicated models")
print(NRMSE_array)



def forceAspect(ax,aspect):
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)



#fig = plt.figure(figsize=(4,1))
#ax=fig    

#plt.figure(figsize = (3.3,2.1))
#plt.figure(figsize = (1.7,1.2))
gs1 = gridspec.GridSpec(2, 2)
gs1.update(wspace=-0.0, hspace=-0.0000) # set the spacing between axes. 


ax = [fig.add_subplot(2,2,i+1) for i in range(4)]
lable=[  "HTris_LArea", "HTris_HArea","LTris_LArea" ,"LTris_HArea"]
for i in range (0,4):

    
    #plt.axis('off')

                
    #subplot_title=(lable[i])

    ax[i] = plt.subplot(gs1[i])
    ax[i].axis('off')
    #ax[i].set_title(subplot_title, fontsize=3, loc='left',y=0.5, pad=17)
    plt.margins(0,0)
    ax[i].imshow(testimage[i], aspect='auto')

plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
fig.subplots_adjust(wspace=0, hspace=0)
plt.gca().set_axis_off()

plt.tight_layout()
plt.savefig("database-screen.pdf", dpi=300, bbox_inches='tight')
plt.show()
plt.close()

'''
dataset2 = pd.read_csv("\\OCT\\tris_dis_gpu_result.csv")

distance2=dataset2['Distance'].values.reshape(-1,1)
gpu2  =dataset2['GPU2'].values.reshape(-1,1)
Tris2  =dataset2['Tris2'].values.reshape(-1,1)
gpu1  =dataset2['GPU1'].values.reshape(-1,1)
Tris1  =dataset2['Tris1'].values.reshape(-1,1)      
label2=['Mixed7 applying simplification'   ,'Mixed7 Baseline']
# create figure and axis objects with subplots()
fig,ax = plt.subplots()

plt.plot(distance2, gpu2,marker="o", color="red",  linewidth=3)
plt.plot(distance2, gpu1,marker="*", color="b" ,linewidth=3)
distance22 = distance2.flatten()

plt.fill_between(distance22, gpu2.flatten(), gpu1.flatten(),
                 facecolor="none", hatch='/', edgecolor="grey")

ax.set_xlabel('Distance')
ax.set_ylabel('GPU_Utilization')

# twin object for two different y-axis on the sample plot

ax2=ax.twinx()
# make a plot with different y-axis using second axis object
ax2.plot(distance2, Tris2,marker="o", color="red")
ax2.plot(distance2, Tris1,marker="*", color="b")
ax2.set_ylabel("Triangles")

plt.legend( label2,loc="lower left",  ncol=1)



plt.show()
plt.tight_layout()
# save the plot as a file
fig.savefig('gpu_tris.pdf',
            dpi=300)
plt.close()
'''
#now read the baseline exp data to generate distance vs gpu -baseline

dataset3= pd.read_csv("\\OCT\\baseline.csv")

gpu4=dataset3['GPU'].values.reshape(-1,1)
distance4  =dataset3['Distance'].values.reshape(-1,1)

i=0
labels4=[]
stored_ind=[]
while(i< len(gpu4)): #start of new case
    
    name=gpu4[i]
    labels4.append(name[0])
    gpu4=gpu4[i+1:]
    distance4=distance4[i+1:]

    tmp=list(gpu4.flatten())

    if(tmp.count(np.nan) !=0):
     index4= tmp.index(np.nan) # found the first nan or space between scenarios
    
    else:
     index4= len(tmp) +1
    
    gpu44=gpu4[0:index4].astype(np.float).flatten()
    
    
    distance44=distance4[0:index4].flatten()
    plt.ylim([0, 100])
    
    value = random.randint(0, 4)
    while(stored_ind.count(value) ): #avoid duplicated elm
      value = random.randint(0, 4)
    stored_ind.append(value)

    #plt.plot(distance44,gpu44 , color=colors[value], marker=markers[value])
   
    i=index4+1
    
    
'''    
plt.xlabel('Distance')  
plt.ylabel('GPU Utilization (%)', labelpad=-3)    
plt.legend( labels4,loc="lower left",  ncol=1, fontsize=11)
  
plt.rcParams['font.size'] = '18'
plt.rcParams['lines.markersize'] = 10
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["axes.labelweight"] = "bold"
plt.savefig('distance_effect.pdf',bbox_inches = 'tight',
            dpi=300)  
plt.show()    
plt.close()
'''

'''
dataset3= pd.read_csv("\\OCT\\raw-texture.csv")

gpu=[]
gpu.append(dataset3['GPU1'].values.reshape(-1,1))
gpu.append(dataset3['GPU3'].values.reshape(-1,1))
gpu.append(dataset3['GPU2'].values.reshape(-1,1))

gpu.append(dataset3['GPU4'].values.reshape(-1,1))
tris  =dataset3['Big_tex'].values.reshape(-1,1)

i=0
labels4=['Big_tex', 'Big_raw', 'Small_tex','small_raw' ]
stored_ind=[]
while(i< len(gpu)): #start of new case
    
    value = random.randint(0, 3)
    while(stored_ind.count(value)): #avoid duplicated elm
      value = random.randint(0, 3)
    stored_ind.append(value)
   
    plt.plot(tris, gpu[i] , color=colors[value], marker=markers[value])
   
    i=i+1
    
    
plt.xlabel('Tris')  
plt.ylabel('GPU ')    
plt.legend( labels4,loc="lower right",  ncol=1)
plt.savefig('tex_raw.pdf',
            dpi=300)    
plt.show()      
plt.close()
'''