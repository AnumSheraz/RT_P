# -*- coding: utf-8 -*-
"""
Created on Fri Dec 02 10:36:43 2016

@author: Anum
"""
import sys, time

def get_CSV_file(file_name):
  with open(file_name, 'r') as f:
    csv_data = []
    for line in f:
            words = line.split(',')
            csv_data.append((words[0:]))
    return csv_data

#Get the file name from command line argument
if len(sys.argv) < 2:
   print "ERROR: Not enough arguments passed"
   print "Usage: Router_patcher <filename>"
   sys.exit() 
else:
   filename = str(sys.argv[1])

try:
  start_tme = time.time() 	
  CSV_data = get_CSV_file(filename)
except:
  print "ERROR: File not found"
  sys.exit()  
    
all_routers = range(1,len(CSV_data)) #list of index of all routers

same_hostnames = [] #holds the index of all routers with same hostname
same_ip = []   #holds the index of all routers with same IPs
valid_routers = []  #holds te index of all valid routers that needs to be patched

######################################################################
#Scanning for all routers with same Username and IP. 
#Scan will run for N(N-1)/2 times. where N=total routers 
# i.e. for 8 routers:
# Outer "for" iteration will run like; 
# compare router 1 with [2, 3, 4, 5, 6, 7, 8]
# compare router 2 with [3, 4, 5, 6, 7, 8]
# compare router 3 with [4, 5, 6, 7, 8]
# compare router 4 with [5, 6, 7, 8]
# compare router 5 with [6, 7, 8]
# compare router 6 with [7, 8]
# compare router 7 with [8]
# compare router 8 with []
for row in range(1,len(CSV_data)):
    checking = all_routers.pop(0)     
    #print checking, all_routers
    for name in range(checking+1, len(CSV_data)):
        #print CSV_data[row][0], ">>", CSV_data[name][0] 
        if CSV_data[row][0].lower() == CSV_data[name][0].lower():
           #print "SAME HOSTnames>>>", CSV_data[row][0], ">>", CSV_data[name][0]
           if (row not in same_hostnames):             
               same_hostnames.append(row)
           if (name not in same_hostnames):
               same_hostnames.append(name)

        if CSV_data[row][1] == CSV_data[name][1]:
           #print "SAME IP>>>", CSV_data[row][0], ">>", CSV_data[name][0]
           if (row not in same_ip):
               same_ip.append(row)
           if (name not in same_ip):
               same_ip.append(name)                 
               
#print same_hostnames
#print same_ip
##########################################################################

for row in range(1,len(CSV_data)):
    if row not in same_hostnames and row not in same_ip: #filtering routers with same username and ip
        for col in range(0,5):
          if CSV_data[row][2].lower() != "yes":  #filtering the routers that have already been patched
             if float(CSV_data[row][3]) >= 12:   #filtering the routers that have older versions than 12           
                #print CSV_data[row][col],
                if row not in valid_routers: 
                   valid_routers.append(row)   

for valid in valid_routers:
   if (len(CSV_data[valid][4]) > 1):      
      print CSV_data[valid][0] + " (" + CSV_data[valid][1] + "), OS version " +  CSV_data[valid][3] + " [" +  CSV_data[valid][4][0:len(CSV_data[valid][4])-1] + "]"  
   else: 
      print CSV_data[valid][0] + " (" + CSV_data[valid][1] + "), OS version " +  CSV_data[valid][3] 
   
total_time = time.time() - start_tme
print "%.6f sec" % (total_time)
#print "Total time:", total_time  , "sec"   
    