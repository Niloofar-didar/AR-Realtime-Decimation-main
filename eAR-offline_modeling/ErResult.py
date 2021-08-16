#from __future__ import print_function
import os
import sys
import time
import argparse
import array as arr 


''' work per object
# gets error data for each object and sorts based on 0.8 - 0,6 till 0.2 ratio in outerror.txt ( input is all error data per object so you need to fetch it manually first from FinalIQA.txt = with this formula: 4 * (distance count) is all error data per objects
'''


#python ErResult.py -- --outm2 inerror.txt
def get_args():
  parser = argparse.ArgumentParser()


  _, all_arguments = parser.parse_known_args()
  double_dash_index = all_arguments.index('--')
  script_args = all_arguments[double_dash_index + 1: ]




# add parser rules
  

  parser.add_argument('-out2', '--outm2', help="Third Object")
  parsed_script_args, _ = parser.parse_known_args(script_args)
  return parsed_script_args
 
args = get_args()

in3 = str(args.outm2)




#opens in3 to read all images for compare, open out to write all results, open IQAout for just one result from ubuntu
with open(in3, "r") as inp, open("outerror.txt", "w") as out:
  


  #numinp=float(inp.readline())
  
  lines = inp.readlines()
  # in each four lines starting from first line, first is for 0.8, next is 0.6, ,04, 0.2... and it repeats so if index of lines array %4==0 it is 0.8 
  ind=0
  j=0;
  counter= len(lines)/4 ; # holds number of error value in each ratio
  while j<4: # holds number of ratios

   ind=j  # in inner for we get error value per each ratio and we go to next ratio
   for i in range(0,counter): 
     out.write(lines[ind])
     ind= ind+4;
   out.write("\n")
   j=j+1;
  
 
  
      

         
        

        

























