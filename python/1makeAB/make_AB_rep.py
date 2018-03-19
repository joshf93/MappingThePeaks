"""Generate popA and popB runs from the initial population, moves them into
a single folder indicated by target_name. Also produces summary CSV for import
into R for graphing and analysis. This script is also used before running
competitions in order to group up the dominant genotypes."""

import sys
import os
import copy
import time
import subprocess
import get_tasks
import mod_env

"""Files that must be in the target directory:
environment_default.cfg file (rename if appropriate, make sure it doesn't have
the header).
events_AB.cfg
sub_org.sub
"""
def make_AB(target_dir):
    #Variables
    
    run_name = target_dir.split("/")[-1]+"_AB"
    run_time = "4:00:00"
    birthy_methody = "0"
    randy_seedy = 14141
    mut_probs = (0.5, 2.0)

    # Crawl the target directory and gather up the dominant files.
    t0 = time.time()
    print("Target dir is:", target_dir)

    # Make a folder to store all the dom files in.
    subprocess.call("mkdir -p dominant", shell = True, cwd = target_dir)

    for folder in os.scandir(target_dir):
        if folder.is_dir() and ("replicate" in folder.name):
            # Catch runs that didn't complete and don't have archive folders.
            try:
                subprocess.call("mv *.org {}.org".format(folder.name),
                                shell=True, cwd="{}/archive".format(folder.path))
            except(FileNotFoundError):
                print("Archive missing! Probably a failed run. Directory is:")
                print(folder.name)
                continue

            copy_cmd = "cp {}/archive/{}.org {}/dominant".format(folder.path,
                                                                  folder.name,
                                                                  target_dir)

            subprocess.check_output(copy_cmd, shell=True,
                                    cwd = "{}/archive".format(folder.path))

    # Grab the statistics from the file. Got the idea from the group's compare.py
    # It's not very elegant though, and you can't use this for logic-80. See if
    # You can think of something better.
    all_orgs = []
    for file in os.scandir("{}/dominant".format(target_dir)):
        if "replicate" not in file.name:
            print("Non replicate file found: {}".format(file.name))
            continue
        org_data = get_tasks.process(file.path)
        all_orgs.append(org_data)

    # Make environment files for each organism.
    subprocess.call("mkdir -p environment_files", shell = True, cwd = target_dir)

    ref_env_file = open("{}/environment.cfg".format(target_dir))
    with open("{}/environment.cfg".format(target_dir), 'r') as ref_env_file:
        ref_env_data = ref_env_file.read()

    #Check to make sure the environment file is properly formatted.
    if "This is the setup file for" in ref_env_data:
        raise ValueError("ERROR: The environment file you're using has the header \
    from the default environment file. It must be removed and the first \
    reaction must be the first line. The environment file you used:\n {}".format(ref_env_data))
    first = True
    for org in all_orgs:
        env_copy = copy.deepcopy(ref_env_data).split('\n')
        # Go through all the pos in task_str, and comment unused ones.
        # Environments with max_count=2 need to go to a special
        # Function for processing. Otherwise, it's a normal run, handle it here.
        """if "max_count=2" in ref_env_data: # Special
            if first:
                print("Using advanced environment processing (tm).")
                first = False
            env_copy = mod_env.modify_environment(env_copy, org)
        else: # Normal"""
        if True:
            if first:
                print("Using normal environment processing.")
                first = False
            for idx, task in enumerate(org[-2]):
                if task == "0":
                    try:
                        env_copy[idx] = "#THIS TASK WAS NOT USED BY THIS ORGANISM"
                    except(IndexError):
                        print("IndexError. Index tried was: {}\n len of env_copy was: {}".format(
                            idx, len(env_copy)))
                else:
                    """This is more complex than it used to be to account for orgs that do a task,
    but do not do it as many times as max_count. Eg. doing not 5 times when max_count is 10."""
                    env_split = env_copy[idx].split("=")
                    env_split[-1] = str(task)
                    env_copy[idx] = '='.join(env_split)

        with open("{}/{}_env.cfg".format(target_dir, org[0].rstrip(".org")), 'w') as env_final_file:
            env_final_file.write("\n".join(env_copy))

    subprocess.call("mv *_env.cfg environment_files", shell = True, cwd = target_dir)

    # Make event files for each organism.
    with open("{}/events_AB.cfg".format(target_dir)) as ref_event_file:
        ref_event_data = ref_event_file.read()

    for org in all_orgs:
        event_copy = copy.deepcopy(ref_event_data)
        event_final = event_copy.replace("ORGANISM_PATH", "../{}/dominant/{}".format(run_name, org[0]))
        with open("{}/{}_events.cfg".format(target_dir, org[0].rstrip(".org")), 'w') as event_final_file:
            event_final_file.write(event_final)

    subprocess.call("mkdir -p event_files", shell = True, cwd = target_dir)
    subprocess.call("mv *_events.cfg event_files", shell = True, cwd = target_dir)

    # Create submission files
    with open("{}/sub_org.sub".format(target_dir), 'r') as ref_sub_file:
        ref_sub_data = ref_sub_file.read()

    # directories
    output_directory = "{}/output".format(run_name)
    data_directory = "../{}".format(run_name)
    data_name = data_directory.lstrip("../")
    eventy_fily = "../{}/event_files".format(run_name)
    envy_fily = "../{}/environment_files".format(run_name)

    for org in all_orgs:
        if org[1] != "1":
            print("Organism was not viable, and was left out:", org)
            continue
        for pop in ("popA", "popB"):
            org_name_noext = org[0].rstrip(".org")
            sub_copy = copy.deepcopy(ref_sub_data)
            sub_copy = sub_copy.replace("SUB_TIME", run_time)
            sub_copy = sub_copy.replace("POPPY", pop)
            sub_copy = sub_copy.replace("OUTPUT_DIRECTORY", "{}/{}/{}".format(output_directory, pop, org_name_noext))
            sub_copy = sub_copy.replace("RANDY_SEEDY", str(randy_seedy))
            randy_seedy += 1
            sub_copy = sub_copy.replace("DATA_NAME", "{}/{}".format(pop, org_name_noext))
            sub_copy = sub_copy.replace("DATA_DIRECTORY", "{}/{}/{}".format(data_directory, pop, org_name_noext))
            sub_copy = sub_copy.replace("EVENTY_FILY", "{}/{}_events.cfg".format(eventy_fily, org_name_noext))

            sub_copy = sub_copy.replace("ENVY_FILY", "{}/{}_env.cfg".format(envy_fily, org_name_noext))
            sub_copy = sub_copy.replace("BIRTHY_METHODY", birthy_methody)

            if pop == "popA":
                mutation_probability = str(mut_probs[0]/int(org[6]))
            else:
                mutation_probability = str(mut_probs[1]/int(org[6]))

            sub_copy = sub_copy.replace("MUTATION_PROBABILITY", mutation_probability)
            if pop == "popA":
                sub_copy = sub_copy.replace("POPUL", str(mut_probs[0]))
            elif pop == "popB":
                sub_copy = sub_copy.replace("POPUL", str(mut_probs[1]))

            with open("{}/{}_{}_sub.sub".format(target_dir, org_name_noext, pop), 'w') as sub_final_file:
                sub_final_file.write(sub_copy)

    subprocess.call("mkdir sub_files", shell = True, cwd = target_dir)
    subprocess.call("mv *_sub.sub sub_files", shell = True, cwd = target_dir)

    # Make a submission script
    sub_script_lines = []
    for file in os.scandir("{}/sub_files".format(target_dir)):
            if file.name.startswith("replicate_"):
                sub_script_lines.append("qsub ./sub_files/{}".format(file.name))

    with open("{}/submit_jobs.sh".format(target_dir), 'w') as sub_script:
        sub_script.write("\n".join(sub_script_lines))

    # Move everything into one folder, nuke the old one if it existed
    subprocess.call("rm -r {}".format(data_name), shell=True, cwd = target_dir)
    subprocess.call("mkdir {}".format(data_name), shell = True, cwd = target_dir)
    subprocess.call("mv dominant {}".format(data_name), shell = True, cwd = target_dir)
    subprocess.call("mv environment_files {}".format(data_name), shell = True, cwd = target_dir)
    subprocess.call("mv event_files {}".format(data_name), shell = True, cwd = target_dir)
    subprocess.call("mv sub_files {}".format(data_name), shell = True, cwd = target_dir)
    subprocess.call("mv submit_jobs.sh {}".format(data_name), shell = True, cwd = target_dir)
    subprocess.call("mkdir output", shell = True, cwd = target_dir+"/{}".format(data_name))
    subprocess.call("mkdir popA", shell = True, cwd = target_dir+"/{}/output".format(data_name))
    subprocess.call("mkdir popB", shell = True, cwd = target_dir+"/{}/output".format(data_name))
    subprocess.call("mkdir popA", shell = True, cwd = target_dir+"/{}".format(data_name))
    subprocess.call("mkdir popB", shell = True, cwd = target_dir+"/{}".format(data_name))

    #Make a csv file for R analysis
    data = ["name, viable, merit, gestation_time, fitness, errors, genome_size,\
    copied_size, executed_size, task_str, task_count"]
    for org in all_orgs:
        holding = ",".join(org)
        data.append(holding)

    with open("{}/{}/run_stats.csv".format(target_dir, data_name), 'w') as stats_file:
        stats_file.write("\n".join(data))

    t1 = time.time()
    print("Done!")
    print("Took {:.2f}s.".format(t1-t0))

if __name__ == "__main__":
    targets = ["/home/josh/archswap/archswap"]

    for targ in targets:
        make_AB(targ)
