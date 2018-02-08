"""Generate files to compete popA and popB at multiple mutation rates to find
the critical value for switching."""

import sys
import os
import copy
import time
import subprocess
import collections
import random
import math

t0 = time.time()

# These are the subdirectories formed by running makeAB on the folders,
# Not the popA/popB folders themselves. 
popA_dir = "/home/josh/flattest_cleanroom/final_run_AB/popA/popA_AB"
popB_dir = "/home/josh/flattest_cleanroom/final_run_AB/popB/popB_AB"
target_dir = "/home/josh/flattest_cleanroom/final_run_alphas"
run_name = target_dir.split("/")[-1]
birthy_methody = "4"
threshold = 1.5 # The min ratio of A/B fitness to be competed.
target_dir_name = "../{}".format(run_name)
key_start =  271828 # Starting seed number
probabilities = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0] # Mut rates to test
run_time = "3:30:00"
run_time_alpha = "03:00:00"
world_size = 3600
min_tasks = 0

# Rename files to avoid conflicts
for pop in (popA_dir, popB_dir):
        for file in os.scandir("{}/dominant".format(pop)):
            if not("popA" in file.name or "popB" in file.name):
                if pop == popA_dir:
                    name = "popA"
                else:
                    name = "popB"
                    
                new_name = "{}_{}.org".format(file.name.rstrip(".org"), name)
                rename_command = "mv {} {}".format(file.name, new_name)
                subprocess.call(rename_command, shell=True, cwd="{}/dominant".format(pop))
 

# Read in the dominant organisms statistics
dom_dict = collections.defaultdict(list)
for pop in (popA_dir, popB_dir):
    with open("{}/run_stats.csv".format(pop), 'r') as stats:
        for line in stats:
            if line.startswith("replicate_"):
                holding = line.split(",")
                if pop == popA_dir:
                    pop_name = "popA"
                else:
                    pop_name = "popB"
                holding.append(pop_name)
                dom_dict[holding[0]].append(holding)

# Entires have form: [name, viable, merit, gestation_time, fitness, errors,
# genome_size, copied_size, executed_size, task_str, pop]

# Check to see which keys have high A:B fitness ratios.
ratio_list = []
exceptional_keys = []
for key in dom_dict:
    #print(key)
    #print(dom_dict[key])
    #input()
    try:
        print("Replicate: {}\nPopA is viable: {} \nPopB is viable: {}".format(key, dom_dict[key][0][1], dom_dict[key][1][1]))
        print("PopA Fitness: {}\nPopB Fitness: {}".format(dom_dict[key][0][4], dom_dict[key][1][4]))
        print("PopA Tasknum: {}\nPopB Tasknum: {}".format(dom_dict[key][0][-2].rstrip("\n"), dom_dict[key][1][-2].rstrip("\n")))
    except IndexError:
        print("Keys unavailable from both populations. One likely didn't complete. Skipping it:", key)
        continue
    if int(dom_dict[key][0][1]) and int(dom_dict[key][1][1]) and \
       float(dom_dict[key][1][4]) > 0.01:
        ratio = float(dom_dict[key][0][4])/float(dom_dict[key][1][4])
        ratio_list.append(ratio)
        print("Ratio:",ratio)
        if ratio > threshold and int(dom_dict[key][0][-2]) > min_tasks:
            print("Exceptional key", key)
            exceptional_keys.append(key)
        print()

print("Ratio list is:\n", ratio_list)  
print("Number exceptional is:", len(exceptional_keys))

# Log the ratio list for plotting.
with open("{}/ratiolst.csv".format(target_dir), 'w') as ratio_file:
        ratio_file.write("\n".join([str(val) for val in ratio_list]))

# Move all of the orgs to the target folder
subprocess.call("mkdir -p organisms", shell = True, cwd = target_dir)
for key in exceptional_keys:
    for pop in (popA_dir, popB_dir):
        if pop == popA_dir:
            population = "popA"
        else:
            population = "popB"
        file_name = "{}_{}.org".format(dom_dict[key][0][0].rstrip(".org"), population)
        cp_command = "cp {} {}/organisms".format(file_name, target_dir)
        subprocess.call(cp_command, shell = True, \
            cwd = "{}/dominant".format(pop))


# Make the event files; Need to change names per run
subprocess.call("mkdir -p event_files", shell = True, cwd = target_dir)
with open("{}/events_compete_AB.cfg".format(target_dir), 'r') as event_ref:
        event_ref_data = event_ref.read()

with open("{}/2p5_alphas_events_AB.cfg".format(target_dir), 'r') as alpha_event:
        alpha_event_ref = alpha_event.read()

for key in exceptional_keys:
    popA_org = "{}/organisms/{}_popA.org".format(target_dir_name, dom_dict[key][0][0].rstrip(".org"))
    popB_org = "{}/organisms/{}_popB.org".format(target_dir_name, dom_dict[key][0][0].rstrip(".org"))
    event_copy = copy.deepcopy(event_ref_data)

    # Go through and randomly shuffle the organisms for injection.
    inject_seq = []
    idxs = []
    for n in range(0,world_size):
        idxs.append(n)    
    random.shuffle(idxs)
    
    for pop in (popA_org, popB_org):
        if pop == popA_org:
            label = 0
            ab = 0
            poplab = 'popA'
        else:
            label = 7
            ab = 1
            poplab = 'popB'
        for _ in range(0,int(math.floor(world_size/2))):
            # Got this process from the previous group's compare.py 
            inject_seq.append("u begin Inject {} {} {} {}\n".format(pop,
                                                                    idxs.pop(),
                                                                    float(dom_dict[key][ab][2])/random.uniform(0.01, 1),
                                                                    label))
        # Handle the alphas event file
        alpha_copy = copy.deepcopy(alpha_event_ref)
        with open("{}/event_files/{}_alphas_{}.cfg".format(target_dir,
                                                           dom_dict[key][0][0].rstrip(".org"),
                                                           poplab), 'w') as event_alpha_out:
                event_alpha_out.write(alpha_copy.replace("INJECTSEQ", pop))


    event_copy = event_copy.replace("INJECTALLSEQS", "".join(inject_seq))
    with open("{}/event_files/{}.cfg".format(target_dir, dom_dict[key][0][0].rstrip(".org")), 'w') as event_out:
        event_out.write(event_copy)

    

# Make the submission files
subprocess.call("mkdir -p sub_files", shell = True, cwd = target_dir)
subprocess.call("mkdir -p competition_data", shell = True, cwd = target_dir)
with open("{}/sub_org_comp.sub".format(target_dir)) as sub_ref:
    sub_ref_data = sub_ref.read()

with open("{}/2p5_sub_org_alphas.sub".format(target_dir)) as alpha_sub_ref:
        sub_ref_alpha = alpha_sub_ref.read()

for prob in probabilities:
    for key in exceptional_keys:
        formatted_name = dom_dict[key][0][0].rstrip(".org")
        sub_copy = copy.deepcopy(sub_ref_data)
        sub_copy = sub_copy.replace("OUTPUT_DIRECTORY", target_dir_name.lstrip("../")+"/output")
        for n in range(0,5): # Make replicates if necessary. Be sure to clean out the sub_file if you don't.
            sub_copy = sub_copy.replace("RANDY_SEEDY{}".format(n), str(key_start))
            key_start += 1
        sub_copy = sub_copy.replace("RUN_NAME", run_name)
        sub_copy = sub_copy.replace("DATA_NAME","{}_{}".format(formatted_name, prob))
        sub_copy = sub_copy.replace("EVENTY_FILY", "{}/event_files/{}.cfg".format(target_dir_name, formatted_name))
        sub_copy = sub_copy.replace("ENVY_FILY", "{}/environment_files/{}_env.cfg".format(target_dir_name, formatted_name))
        sub_copy = sub_copy.replace("BIRTHY_METHODY", birthy_methody)
        sub_copy = sub_copy.replace("MUTATION_PROBABILITY", str(prob/float(dom_dict[key][0][6])))
        sub_copy = sub_copy.replace("SUB_TIME", run_time)
        with open("{}/sub_files/{}_{}.sub".format(target_dir, formatted_name, prob), 'w') as sub_out:
            sub_out.write(sub_copy)

        # Alpha
        for pop in ("popA", "popB"):
                if popA_dir == popB_dir and pop == "popB":
                        continue
                alpha_sub_copy = copy.deepcopy(sub_ref_alpha)
                # Make replicates.
                for n in range(0,20):
                    alpha_sub_copy = alpha_sub_copy.replace("RANDY_SEEDY{} ".format(n), str(key_start)+" ")
                    key_start += 1
                alpha_sub_copy = alpha_sub_copy.replace("RUN_NAME", run_name)
                alpha_sub_copy = alpha_sub_copy.replace("DATA_NAME","{}_{}_alphas_{}".format(formatted_name, prob, pop))
                alpha_sub_copy = alpha_sub_copy.replace("EVENTY_FILY", "{}/event_files/{}_alphas_{}.cfg".format(target_dir_name, formatted_name, pop))
                alpha_sub_copy = alpha_sub_copy.replace("ENVY_FILY", "{}/environment_files/{}_env.cfg".format(target_dir_name, formatted_name))
                alpha_sub_copy = alpha_sub_copy.replace("BIRTHY_METHODY", birthy_methody)
                alpha_sub_copy = alpha_sub_copy.replace("MUTATION_PROBABILITY", str(prob/float(dom_dict[key][0][6])))
                alpha_sub_copy = alpha_sub_copy.replace("SUB_TIME", run_time_alpha)
                with open("{}/sub_files/{}_{}_alpha_{}.sub".format(target_dir, formatted_name, prob, pop), 'w') as alpha_sub_out:
                    alpha_sub_out.write(alpha_sub_copy)

# Make the qsub script
jobs = []
alphajobs = []
for sub in os.scandir(target_dir+"/sub_files"):
    if sub.is_file() and "replicate" in sub.name:
                if "alpha" in sub.name:
                    alphajobs.append("qsub ./sub_files/{}".format(sub.name))
                else:
                            jobs.append("qsub ./sub_files/{}".format(sub.name))

with open("{}/submit_comp.sh".format(target_dir), 'w') as comp_file:
    comp_file.write("\n".join(jobs))

with open("{}/submit_comp_alphas.sh".format(target_dir), 'w') as comp_file:
            comp_file.write("\n".join(alphajobs))

# Move the environment files
source = "/".join(popA_dir.split("/")[0:len(popA_dir.split("/"))-2])
print(source)
subprocess.call("cp -r {}/environment_files .".format(source), shell=True, cwd=target_dir)

# Make output directory
subprocess.call("mkdir output", shell=True, cwd=target_dir)


