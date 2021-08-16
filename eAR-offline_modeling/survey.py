"""
Created on Thu Jan 28 10:31:21 2021
GENERATE SCREENSHOTS SIDE BY SIDE +



@author: 
"""

""
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import csv
import statistics
import math 
from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib import pyplot as plt
from matplotlib import pyplot as plt2

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import cv2
import numpy as np
'''
START sECTION FOR SURVEY GRAPHS 
READS FROM MODEL.TXT WHICH IS OUTPUT FOR SCREEN SHOTS OF TEST.PY IN LIBMSD DIRECTORY

'''


with open("Objects/finalObj/qualities.txt", "r") as inp, open("survey/filename.txt", "w") as out:
 
 
    
  lines = inp.readlines()
  
  i=0
  index=0
  objcount= len(lines)/12
  
  
  object_index =0 # points to the first distance of each object
  
  while(object_index< len(lines)):
  
   for dis in range(0,3): # three distances
    
    token1=lines[object_index+ dis] # first distance to third one
    img= cv2.imread(token1[:-1])
       
    for factors in range (1,4): # 1,4 ->3 screenshots per each object (1 and 0.2, 1 and 0.4, one and 0.6)
   
   


      token2= lines[object_index+ dis+ (factors*3)]
      #img2 = mpimg.imread(token2[:-1])
      img2= cv2.imread(token2[:-1])
      # print (str(token1) + ", " +str(token2) )
    
   #one inch is 80 pixel so 960* 540  pixel is (960 / 80) 540/80 
      
      im_v = cv2.vconcat([img, img2])
      
      #plot_image = np.concatenate((img, img2), axis=0) # horizantally axis =1

      
      address=token2[17:-5]
      print(address)
      fig = plt.figure(figsize=(50, 50))
      
      cv2.imwrite("survey/" +address +".png", im_v)
      out.write(address +".png"+"\n")
      plt.close()
      #plt.imshow(im_v)
      #plt.imshow(plot_image)
      #plt.savefig("survey/" +address +".png")
      

      #plt.show()

   object_index+=12            
