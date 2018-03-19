import sys
import os
import copy
import time
import subprocess

target_dir = "/home/josh/flattest_cleanroom/final_run_landscape_long/data"

a_list = []
b_list = []

for file in os.scandir(target_dir):
    if "step" in file.name:
        data = open(file.path)
        target = ""
        for line in data:
            if line[0] != "#" and line[0] != "\n":
                target = line
                break
        
        if "1step" in file.name:
            target = target.rstrip("\n") + " " + file.name[0:14] + " " + "1one\n"
        elif "2step" in file.name:
            target = target.rstrip("\n") + " " + file.name[0:14] + " " + "2two\n"
        elif "3step" in file.name:
            target = target.rstrip("\n") + " " + file.name[0:14] + " " + "3three\n"
        elif "4step" in file.name:
            target = target.rstrip("\n") + " " + file.name[0:14] + " " + "4four\n"
        else:
            target = target.rstrip("\n") + " " + file.name[0:14] + " " + "5five\n"
 

        if "popA" in file.name:
            target = target.rstrip("\n") + " " + file.name[0:14] + " " + "popA\n"
            a_list.append(target)
        else:
            target = target.rstrip("\n") + " " + file.name[0:14] + " " + "popB\n"
            b_list.append(target)
        
    
a_details = open(target_dir+"/final_run_landscape_long_Fit.dat", 'w')
b_details = open(target_dir+"/final_run_landscape_long_Flat.dat", 'w')

a_details.write("".join(a_list))
a_details.close()
b_details.write("".join(b_list))
b_details.close()
