# -*- coding: utf-8 -*-
#   

# this is to calculate regression model for degradation error , finding RMSE error and percentage error by chrval parameters, gamma and max distance
'''

gets the model degradation error and distance and gives the degradation model parameters and graphs

reads from all models in testvalue.csv and write information in degmodel.csv

@@@ instruction
1- for deg model plot uncomment line  453-457 + 662-670 , and comment  line 680-687 lines 586 + 577-578 
2- for error bar uncoment line 680-687 lines 586 + 577-578  and comment  line  453-457 + 662-670 ,
modified regmodel for all objects where we can add  data for all objects to get their relative model
@@@ instruction

we can obseve that as gamma is smaller and closer to gamma1, the predicted model is closer to actual data in the closer distances and as gamma becomes bigger, the predicted model is more closer to real data in farthesst distances. 
for gamma=gamma1 we can make distance confined to distance =20 as an eg ( or by  measuring virtual siize for object we can find a fixed ratio for distance that makes all object similar in terms of size and correspondingly calculate maximum confined distance for each one -> actually we have this feature already as max distancef ro each object, we just need to change ratio to make max distance lower.
'''
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import csv
import statistics
import math 
from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib import pyplot as plt
from matplotlib import pyplot as plt2
import os.path
from os import path
from matplotlib import rcParams

plt.rcParams.update({'font.size': 15})
#markers = ['>', '+', '.', 'o', 'v', 'x', 'X', '|','^','<','s','p','|'
markers = ['>', '+',  'o', 'v', '3','X','^','s','*','2', 'd','h','<']
exist=False
colors=[  'gold' , 'b', 'g', 'red', 'darkorange', 'darkorchid','navy','blueviolet','teal','lightcoral' ,'olive', 'grey',  'firebrick','deeppink','lawngreen','slategrey']
bold=1
address='Nov\\Nov3 and 4\\degmodel_file.csv'
if(path.exists(address)):
    
  exist=True

first=0
fig, ax = plt.subplots()
stored_distance=[[]]
stored_deg2=[[]]
stored_ind=[]
#read in the file
#dataset = pd.read_csv("C:\\Users\\loaner\\Desktop\\newValues.csv")
dataset = pd.read_csv("Nov\\Nov3 and 4\\one_deg.csv")
reader = csv.DictReader(open("Nov\\Nov3 and 4\\one_deg.csv"))
tris_dataset = pd.read_csv("Nov\\Nov3 and 4\\tris_fileseize.csv")

tris = tris_dataset['Tris'].values.reshape(-1,1) # points to the fillee with all objects
o_name = tris_dataset['name'].values.reshape(-1,1)
o_size = tris_dataset['size'].values.reshape(-1,1)

objectname=[]
headerNames = []
file2 = open("Errors.txt","a+") 
file1 = open("SUM_Errors.txt","a+")
for i in reader.fieldnames:
    headerNames.append(i)

#length = len(headerNames)   #size of the original row headers

#epochs=length/6 # to the num of obj data
j=1

distance1 = (dataset['distance'].values.reshape(-1,1))
name1=dataset['name'].values.reshape(-1,1)
list11=(dataset['0.2'].values.reshape(-1,1))
list44=(dataset['0.4'].values.reshape(-1,1))
list66=(dataset['0.6'].values.reshape(-1,1))
list88=(dataset['0.8'].values.reshape(-1,1))

lines=[ ".",  "dashed", "solid", "dashdot",   ':']


objname=[]
dist=[]
list22=[]
list444=[]
list666=[]
list888=[]
for i in range(0, len(name1)):
    objname.append(str(name1[i][0]))
    list22.append(float(list11[i]))
    list444.append(float(list44[i]))
    list666.append(float(list66[i]))
    list888.append(float(list88[i]))
    dist.append((distance1[i]))

'''dist, list11, list22, objname, name1m distance1 .. all aare using index that is defined in the next two lines later'''


#print(objname[0] )
print( str(name1[0][0]))
print( float(distance1[0]))
count= distance1[len(distance1)-1] #num of objects
distance1=distance1[:len(distance1) -1]

mindis =[]
stored_ind2=[]
labels=[]
labels2=[]
#fig2 = plt2.figure(figsize=(4,3))
#fig = plt.figure(figsize=(6.5,4.5))
with open('Nov\\Nov3 and 4\\degmodel_file.csv', mode='+a',newline='') as degmodel_file:
 file_writer = csv.writer(degmodel_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
 if(exist==False):
      file_writer.writerow(['alpha','betta','c','gamma','max_deg','tris','name','mindis', 'filesize'])
 
 counter2=0
 objects= np.arange(int(count)) 
 for ep in range(0, int(count)):

     
  all_nrmses=[]
  name=objname[counter2+1]
  #if (objname[27] == "Cabin"):
  repetative=False

  print(name) 
  index=objname.index(name)
  while(index<len(objname) and objname[index]==name):
      index+=1
  
  
  
  multipleMultivariate = []

  first_regression = []
  second_regression = []
  third_regression = []
  final_regressionList = []
  newHeaders = []             #list to hold only the ratio values


  distance = dist[counter2:index]
  
  Nilname=[]
  first_indexin_newdata=0
  tmpname=dataset['name'].values.reshape(-1,1)
  for i in range(0, len(name1)):
    if(name== str(tmpname[i][0])):
        first_indexin_newdata=i
        break
    
    
  size=len(dataset.index)
  dataset= dataset.iloc[first_indexin_newdata:size,0:6]
  dataset=dataset.reset_index(drop=True) 
  #df_r = df.reset_index(drop=True)
  mindis.append(distance[0])
#gammaList = dataset['gamma'].values.reshape(-1,1)


#gamma = gammaList[0]

  counter = 1
  gamma_values = []
  filesize_values=[]
  
  #objname=dataset['name'+str(ep)].values.reshape(-1,1)
  list2=[]
  list1=[]
  list4=[]
  list6=[]
  list8=[]
#Nill change
  list1=  list11[counter2:index]
  list2= list22[counter2:index]
  list4= list444[counter2:index]
  list6= list666[counter2:index]
  list8= list888[counter2:index]
  #dataset['0.2-'+str(ep)].values.reshape(-1,1)
  
  
  #row_count = sum(1 for row in reader)
  
  norm_list6=[]
  
  for i in range (0, len(list6)):
      norm_list6.append(list6[i]/(list2[0] ))
      
  min_norm=list8[len(list8)-1] 
  max_norm=max (list2[0], list4[0],list6[0])
  
  row_count = len(distance)
  gamma_1 = math.log ( list2[0]/list2[1], distance[1]/distance[0])
  gamma_2 = math.log ( list2[0]/list2[row_count-1], distance[row_count-1]/distance[0])

  gamma= (gamma_1 +gamma_2) /2
 

  gamma_values.append(gamma_1)
  gamma_values.append(gamma_2)
  gamma_values.append(gamma)
  ratio_list = []
  r=0
  for i in range( 0,4):
    ratio_list.append(round(r+0.20,2))
    r+=0.20
  '''
  if (name =="plane" or name =="Cabin"):
  
   stored_distance.append(distance)
   stored_deg2.append(list2)
   #stored_ind.append(name)
   '''   
   
  value = random.randint(0, len(markers)-1)
  while(stored_ind.count(value)): #avoid duplicated elm
      value = random.randint(0, len(markers)-1)
   
  #if ( name!= "CocacolaFinal"  ):
  if ( name!= "CocacolaFinal" and name != 'BigCabin' and name!= 'drawer' ): 
      
   if(name=="Cabin"):
     name="cabin"
   if(name!="table" ):
     labels.append(name)
     stored_ind.append(value)
  #stored_ind.append(name)


  if(name=="cabin"):
     name="Cabin"
  file3=open("SUM_Errors.txt","r")
  data=[]
  data=file3.readlines()
  xx=0
  while(xx< len(data)):
      if (data[xx][:-1]==name):
          print ("data already exist")
          repetative=True
      xx+=4
  
    
  if(repetative==False):
    file2.write(str(objname[index-1])+"\n")
  
  
  
  print ("gamma1  is " + str(gamma_1) )
  print ("gamma2  is " + str(gamma_2) )
  print ("gamma_avg  is " + str(gamma) )



  distance_list = []
  Y = []


  for x in distance:
        distance_list.append(x)
        

  for i in ratio_list: # in ratios
    error_current = dataset[str(i)].values.reshape(-1,1)
    for x in range(0,row_count):
        Y.append(error_current[x] )# Y is actual normalized error
        

  z1 = []
  z2 = []
  z3 = []

  tempZ3 = []

  for gamma_current in gamma_values:

    z1 = []
    z2 = []
    z3 = []
    
    tempZ3 = []
    
    for e in ratio_list:
        
        counter = 0
        for i in distance:
            value = (1 / ((distance[counter])**gamma_current))
            if counter < row_count:
                z3.append(value)
                tempZ3.append(value)
                counter = counter + 1
                
        counter = 0
        
        
    
        for i in tempZ3:
            value = float(e)*float(e)*i
            z1.append(value)
            counter = counter + 1
            
        counter = 0
        for i in tempZ3:
            value = i*float(e)
            z2.append(value)
            counter = counter + 1
            
        tempZ3.clear()
        
        X = [z1,
             z2,
             z3]
    

    
    Ya = np.array(Y)
    Xa=np.array(X).transpose()[0]
    reg = LinearRegression(fit_intercept=False).fit(Xa, Ya)
    
    coeffs=reg.coef_.tolist()
    coeffs.append(reg.intercept_)
    
    
    coeffs = [ round(elem, 4) for elem in coeffs[0] ]
    
    print('Multivariate Linear Regression Coefficients: ',coeffs)
    
    a = coeffs[0]
    b = coeffs[1]
    c = coeffs[2]
    
    multipleMultivariate.append(a)
    multipleMultivariate.append(b)
    multipleMultivariate.append(c)



  lowestError = []
  lowestErrorValue = 0
  determineGamma = []
  List_meanof_percerror=[]
  print()
  print()

  first_regression.append(multipleMultivariate[0])
  first_regression.append(multipleMultivariate[1])
  first_regression.append(multipleMultivariate[2])

  second_regression.append(multipleMultivariate[3])
  second_regression.append(multipleMultivariate[4])
  second_regression.append(multipleMultivariate[5])

  third_regression.append(multipleMultivariate[6])
  third_regression.append(multipleMultivariate[7])
  third_regression.append(multipleMultivariate[8])

  final_regressionList.append(first_regression)
  final_regressionList.append(second_regression)
  final_regressionList.append(third_regression)


  counter = 1
  newCounter = 0
  current_gamma = 0


  for current_coefficient in final_regressionList:
    
    a = current_coefficient[0]
    b = current_coefficient[1]
    c = current_coefficient[2]
    
    
    current_gamma = gamma_values[newCounter]
    lowestErrorValue = 0
    lowestError = []
    lowest_perc_err=[]
    print(counter,".", "CURRENT GAMMA BEING USED: ", current_gamma, "    current Regression being used: ", current_coefficient )
    print()
    for j in ratio_list: # fo all ratios we have
      model_values = []
      list2=[]
      new_distance=[]
      #j=j.split("-")[0]
      ratio = float(j)
    ############################################################
    #Nil 16 sep
    
      #for i in distance:
      interval=2

      max_distance= 30
      
      for i in range(0, row_count-4, interval):
    
        if ( distance[i] <=max_distance) : 

         denom = distance[i]**current_gamma

        #Nil - correction in formula
         result = (((a*(ratio**2))+(b*ratio)+(c)) / (denom))
         model_values.append(result)
        else:
            break
      y_pred = model_values
    
      for i in range(0, row_count-4, interval):
        if ( distance[i] <=max_distance) : 
         list2.append( dataset[str(ratio)].values.reshape(-1,1) [i])
         new_distance.append( distance[i])
        else:
            break
    
     

      y_true = np.array(list2)
    

      mse= mean_squared_error(y_true, y_pred)
      rmse = np.sqrt(mse)
      nrmse= rmse/ (max_norm-min_norm)
      lowestError.append(nrmse) # has nrmse for each ratio of the current gamma
      
      
      if(repetative==False):
        file2.write('NRMSE (no intercept): {}'.format(nrmse)+"\n")
        file2.write("percentage error for ratio "+ str(ratio)+ " is " + str(np.mean(np.abs((y_true - y_pred) / y_true)) * 100)+"\n")
      print('NRMSE (no intercept): {}'.format(nrmse))
    
      print("percentage error for ratio "+ str(ratio)+ " is " + str(np.mean(np.abs((y_true - y_pred) / y_true)) * 100))
      lowest_perc_err.append(np.mean(np.abs((y_true - y_pred) / y_true) * 100))
    
        
    
    # nil 16 sep
    #############################################3

    all_nrmses.append(lowestError)
    
    lowestErrorValue = statistics.mean(lowestError) #mean of NRMSE among 4 dec ratio for the three gammas
    mean_perc_error= statistics.mean(lowest_perc_err)
    
    determineGamma.append(lowestErrorValue)
    List_meanof_percerror.append(mean_perc_error)
    
    
    denom = distance[i]**current_gamma
    result = (((a*(ratio**2))+(b*ratio)+(c)) / (denom))
    
    if(repetative==False):
      file2.write("Average NRMSE error: "+ str( lowestErrorValue)+"\n")
    
    print("Average NRMSE error: "+ str( lowestErrorValue))

    '''for deg model un comment'''
    #plt.rc('font', size=5) 
    #plt.xticks(distance)
    #plt.plot(new_distance, model_values) # both should have same dimension
    '''for deg model un comment'''
    
    print()
    counter = counter + 1
    newCounter = newCounter + 1




  indx = 0
  temp = List_meanof_percerror[0] # has mean of perc_erro for  all ratios of three gammas
  for i in range(0,len(List_meanof_percerror)):
    if temp > List_meanof_percerror[i]:
        temp = List_meanof_percerror[i]
        indx = i

  indx = indx % 3
  print("Lowest AvG Percentage_err out of all the Gamma values: ", temp, " for Gamma value:", gamma_values[indx])
  if(repetative==False):
    file1.write(str(objname[index-1])+"\n")
    file2.write("Lowest AvG Percentage_err out of all the Gamma values: "+ str(temp)+ " for Gamma value:"+ str(gamma_values[indx])+"\n")
    file1.write("Lowest AvG Percentage_err out of all the Gamma values: "+ str(temp)+ " for Gamma value:"+ str(gamma_values[indx])+"\n")
    
    
  indx = 0
  temp = determineGamma[0]
  for i in range(0,len(determineGamma)):
    if temp > determineGamma[i]:
        temp = determineGamma[i]
        indx = i

  indx = indx % 3
  best_mean_nrmse=temp # this is the minimum of three average nrmse
  print("Lowest AvG NRMSE out of all the Gamma values: ", best_mean_nrmse, " for Gamma value:", gamma_values[indx])
  

  if(name=="GarbageFinal"):
          name="Garbage"
    
  if(name=="Cabin"):
          name="cabin" 
  if(name=="CocacolaFinal"):
          name="coke" 
  
  if(repetative==False):

    file2.write("Lowest AvG NRMSE out of all the Gamma values: "+ str(best_mean_nrmse)+ " for Gamma value:"+str( gamma_values[indx])+"\n")
    file1.write("Lowest AvG NRMSE out of all the Gamma values: "+ str(best_mean_nrmse)+ " for Gamma value:"+str( gamma_values[indx])+"\n")
  
 #stores all rmses
    
    
    file1.write("\n")
    file2.write("\n")
  z1 = []
  z2 = []
  z3 = []

  for e in ratio_list:
    #e=e.split("-")[0]
    counter = 0
    for i in distance:
        value = (1 / ((distance[counter])**gamma_values[indx]))
        if counter < row_count:
            z3.append(value)
            tempZ3.append(value)
            counter = counter + 1
            
    counter = 0
    
    

    for i in tempZ3:
        value = float(e)*float(e)*i
        z1.append(value)
        counter = counter + 1
        
    counter = 0
    for i in tempZ3:
        value = i*float(e)
        z2.append(value)
        counter = counter + 1
        
    tempZ3.clear()
    
    X = [z1,
         z2,
         z3]




  Ya = np.array(Y)
  Xa=np.array(X).transpose()[0]
  reg = LinearRegression(fit_intercept=False).fit(Xa, Ya)

  coeffs=reg.coef_.tolist()
  coeffs.append(reg.intercept_)


  coeffs = [ round(elem, 4) for elem in coeffs[0] ]
  print("data for obj "+ str(ep) + ": ")

  print("based on NRMSE values,")
  print('Most Accurate Multivariate Linear Regression Coefficients: ',coeffs)
  #j=k+1
  #k+=6
  
  o_name2 = o_name.tolist()
  obj_indx= o_name2.index(name1[index-1]) # search deg model obj name in lis of objects to find the index for tris
  
  if(repetative==False):
    
    
    file_writer.writerow([coeffs[0], coeffs[1],coeffs[2],gamma_values[indx],float(list1[0]), float(tris[obj_indx]),str(objname[index-1]), float(mindis[ep]), float(o_size[obj_indx]) ])
  
  counter2=index
  if (ep<5 ):
    obj_std=np.std(all_nrmses[indx])
    '''
   # uncomment for error bar
    #ax.bar(first,temp,yerr=obj_std, edgecolor = "black", align='center',alpha=1,color='darkgray',ecolor='red', capsize=10)
    '''
    objectname.append(name)
    first+=1

  elif ( name =="chair" or name =="plane" or name=="apricot" or name=="ATV"):
   obj_std=np.std(all_nrmses[indx])
   '''uncomment for error bar
   #ax.bar(first,temp,yerr=obj_std, edgecolor = "black", align='center',alpha=1,color='darkgray',ecolor='red', capsize=10)
   '''
   objectname.append(name)
   first+=1


# 

#  This is to show deg model you need to uncomment the plt. in above     =============================================================================
# ax = plt.gca()      
# 
# ax.set_xscale('log')  
# 
# plt.xlabel('Distance',labelpad=-1)  
# plt.ylabel('Degradation_Error')
# leg = ax.legend();
# plt.legend( labels, loc="upper center", bbox_to_anchor=(0.89,1 ), fontsize=10)
# plt.tight_layout()
# plt.savefig("deg_er.pdf", dpi=300, bbox_inches = 'tight')
# 
# plt.show()
# =============================================================================

# start plotting the trained model and actual mmodel

  for j in ratio_list: # fo all ratios we have
  
    if ((j==0.4 or j==0.8) and (name =="splane" or name =="cabin")):
      model_values = []
      actual_model=[]
      new_distance=[]
     
      ratio = float(j)
  
      interval=1

      max_distance= 40
      
      max_norm20=(((a*(0.2**2))+(b*0.2)+(c)) / (distance[0]** gamma_values[indx]))
      max_norm40=(((a*(0.4**2))+(b*0.4)+(c)) / (distance[0]** gamma_values[indx]))
   
      max_normalized_weigth = max(max_norm20,max_norm40)
      min_normalized_weigth= (((a*(0.8**2))+(b*0.8)+(c)) / (distance[len(distance)-1]** gamma_values[indx]))
    
      for i in range(0, row_count-4, interval):
    
        if ( distance[i] <=max_distance) : 

         denom = distance[i]** gamma_values[indx] # uses the best gamma in terms of rmse
         result = (((a*(ratio**2))+(b*ratio)+(c)) / (denom))/(max_normalized_weigth )
         model_values.append(result)
        else:
            break
      y_pred = model_values
    
    
    
      for i in range(0, row_count-4, interval):
        if ( distance[i] <=max_distance) : 
         actual_model.append( dataset[str(ratio)].values.reshape(-1,1) [i]/(max_norm ))
         new_distance.append( distance[i])
        else:
            break
    

      

 
      value1 = random.randint(0, len(markers)-1)
      value2 = random.randint(0, len(markers)-1)
      while(stored_ind2.count(value1) ): #avoid duplicated elm
        value1 = random.randint(0, len(markers)-1)
      stored_ind2.append(value1) 
      while(stored_ind2.count(value2) ): #avoid duplicated elm
         value2 = random.randint(0, len(markers)-1)
      stored_ind2.append(value2)  
# =============================================================================
#        for deg training model=== un comment
#=============================================================================
      '''# for deg training model= '''      
      plt2.plot(new_distance,actual_model, marker= markers[value1], color=colors[value1],linestyle="None") # plotting t, a separately 
      labels2.append(name + "_real_"+ str(round(1-j,2)))
      plt2.plot(new_distance,y_pred #, linewidth=bold
                ,color=colors[value1],linestyle=lines[bold]) # plotting t, a separately 
      labels2.append(name + "_pred_"+ str(round(1-j,2)))  
      bold+=1
#=============================================================================
 '''# for deg training model'''  
     
 
    
'''# for error bar'''      
# 
# =============================================================================
# =============================================================================
# for error bar
# =============================================================================
# ax.set_xticks(objects[0:len(objectname)]) # define points up to the length of names we added
# ax.set_xticklabels(objectname)
# ax.set_ylabel('NRMSE')
# ax.yaxis.grid(True)
# plt.tight_layout()
# plt.savefig("deg_trained_error.pdf", dpi=300, bbox_inches = 'tight')
# plt.show()
# =============================================================================
# 
# =============================================================================
'''# for error bar'''  

file2.close()
file1.close()
file3.close()



# =============================================================================
# for deg training model === un comment
# =============================================================================
ax2 = plt2.gca()      
ax2.set_xscale('log')  
#y = np.arange(0, 1.2, 0.2)
plt.ylim([0, 1])
ax2.tick_params(axis='x', pad=-3)
rcParams['xtick.major.pad']='-3'
plt2.xlabel('Distance', labelpad=(-2))  
plt2.ylabel('Degradation_Error')
plt2.legend( labels2, loc="upper center", bbox_to_anchor=(0.84,1 ), fontsize=10)
plt2.tight_layout()
plt2.rcParams['font.size'] = '18'
plt2.rcParams['lines.markersize'] = 10
plt2.rcParams["font.family"] = "Times New Roman"
plt2.rcParams["axes.labelweight"] = "bold"
plt2.savefig("trained_deg.pdf", dpi=300, bbox_inches = 'tight')
# # 

plt2.show()
# 
# =============================================================================




