"""Gathers up the avg, dom, etc. files from the replicate runs and merges them
for analysis in R or other programs. Includes some extra convenience data such
as fitness after initial phase and pseudogeneration for keeping track of
generations."""

import sys
import os
import copy
import time
import subprocess
import argparse

def split_alpha(filename):
    #replicate_015762_4.5_alphas_popA_r9
    filename_split = filename.split("_")
    repid = "{}_{}".format(filename_split[0], filename_split[1])
    mutrate = filename_split[2]
    repnum = filename_split[-1]

    ssv = "{} {} {}".format(repid, mutrate, repnum)
    return(ssv)
    
    

def merge_folder_data(target_dir, org_folder, destination_dir):
    target_filenames = ["dominant.dat", "average.dat", "data.dat", "variance.dat"]
    output_filename = "{a}_{b}_{c}.dat".format(a=target_dir.split("/")[-2], b=target_dir.split("/")[-1], c="{}")
    
    
    for targ in target_filenames:
        out_list = []
        # Append some info to the beginning for logging purposes.
        out_list.append("#The target_dir was: {}\n#org_folder was: {}\n\
        #target_filename was: {}\n#output_filename was: {}\n".format(target_dir,
                                                                  org_folder,
                                                                  targ,
                                                                  output_filename.format(targ[0:3])))

        for folder in os.scandir(target_dir):
            if "replicate" not in folder.name:
                continue
            for file in os.scandir(folder.path):
                if targ in file.name:
                    try:
                        with open("{}/{}/archive/{}.org".format(target_dir,
                                                                folder.name,
                                                                folder.name)) as org_file:
                            for line in org_file:
                                if "Fitness.." in line:
                                    line_split = line.split()
                                    fitness = line_split[2]
                                    break
                    except FileNotFoundError:
                        #print("Couldn't find organism for {}, skipping.".format(folder.name))
                        #print("Path searched was: {}".format("{}/{}/archive/{}.org".format(org_folder, folder.name, folder.name)))
                        fitness = "NA"
                        continue
                    with open(file.path) as data:
                        datalines = data.read()
                        
                    datalist = datalines.split('\n')
                    target = ""
                    temp = []
                    counter = 0
                    
                    if len(out_list) == 1: # Grab header from the first file
                        for line in datalist:
                            if line.startswith("#"):
                                temp.append(line+"\n")

                    for line in datalist: # Grab the data but skip the header
                        if not line.startswith("#") and not line.startswith("\n") and line:
                            if "alpha" in folder.name:
                                repname = split_alpha(folder.name)
                            else:
                                repname = folder.name
                            line = "{} {} {} {}\n".format(line.rstrip("\n"),
                                                          repname, fitness, counter)
                            temp.append(line)
                            counter += 1
                    out_list.append("".join(temp))

        with open("{}/{}".format(destination_dir, output_filename.format(targ[0:3])), 'w') as of:
            of.write("".join(out_list))
            

if __name__ == "__main__":
    target_dirs = ["/home/josh/flattest_cleanroom/final_run_AB_makeup/popB"]
    org_folder =  "/home/josh/flattest_cleanroom/final_run_AB/dominant"
    destination_dir = "/home/josh/flattest_cleanroom/final_run_AB_makeup/popB"
    for target in target_dirs:
        merge_folder_data(target, org_folder, destination_dir)

    
    """
    #This is for a specific run.
        for folder in os.scandir(target_dir):
        for pop in ("popA", "popB"):
            merge_folder_data("{}/{}".format(folder.path, pop),
                              org_folder, destination_dir)
    """
    print("Done!")
