"""Takes an avida archive directory and sets up alpha runs for all of them."""
import os
import sys
sys.path.append(os.path.abspath("/home/josh/Link to MappingPeaks/Reference files/verif/1makeAB"))
import get_tasks
from collections import defaultdict
import subprocess
import copy

def newest_org(org_dict):
    """Returns the "newest" org; the one that was printed nearest the
end of the run. Ensures things are ordered before running."""
    # There's probably a more elegant way to do this, but it works.
    update = -1
    maxkey = None
    for key, value in org_dict.items():
        if value['update'] > update:
            update = value['update']
            maxkey = key
    if maxkey is None:
        raise ValueError("No update value greater than zero was found during newest_org. {}".format(org_dict))

    return(org_dict[maxkey])


def read_update(org_data):
    # Grab the update at which an org was written.
    update_str = "# Update Output...: "
    org_data_split = org_data.split("\n")
    for line in org_data_split:
        if line.startswith(update_str):
            try:
                update = int(line.lstrip(update_str))
            except ValueError:
                #print("Org's update entry is N/A: {}".format(org_path))
                update = 0
                
            return(update)


def read_orgs(path):
    # Read all organisms in a directory into a dictionary.
    org_dict = defaultdict(dict)
    for org in os.scandir(path):
        if org.is_file() and org.name.endswith(".org"):
            org_dict[org.name]['file_handle'] = org
            with open(org.path, 'r') as org_file:
                org_dict[org.name]['file_data'] = org_file.read()
            org_dict[org.name]['update'] = read_update(org_dict[org.name]['file_data'])
            org_dict[org.name]['statistics'] = get_tasks.process(\
            org_dict[org.name]['file_handle'].path)
            org_dict[org.name]['name'] = org.name
            org_dict[org.name]['newname'] = "replicate_{:06d}".format(org_dict[org.name]['update'])
  
    return(org_dict)

def make_env_files(org_dict, env_path):
    # Makes the environment files for each organism.
    
    with open(env_path, 'r') as env_file:
        env_reference = env_file.read().split('\n')

    # Check to make sure we're not using a malformed file.
    if "This is the setup file for" in env_reference:
        raise ValueError("ERROR: The environment file you're using has the header \
        from the default environment file. It must be removed and the first \
        reaction must be the first line. The environment file you used:\n {}".format(ref_env_data))

    for key, org_entry in org_dict.items():
        env_copy = copy.deepcopy(env_reference)
        task_str = org_entry['statistics'][-1]
        for idx, task in enumerate(task_str):
            if task == "0":
                env_copy[idx] = "#THIS TASK WAS NOT USED BY THIS ORGANISM aot"
        org_entry['env_file'] = "\n".join(env_copy)


def make_event_files(org_dict, event_path, target_path):
    # Make the event file entries.
    with open(event_path, 'r') as event_file:
        event_reference = event_file.read()

    for key, org_entry in org_dict.items():
        event_copy = copy.deepcopy(event_reference)
        event_copy = event_copy.replace("ORGANISM_PATH", "{}/{}".format(target_path, org_entry['name']))
        event_copy = event_copy.replace("INJECTSEQ", "{}/{}".format(target_path, org_entry['name']))
        org_entry['event_file'] = event_copy

"""      
def make_sub_files(org_dict, sub_path, run_name key_start = 1000):
    #MANUAL MODE FOR NOW
    with open(sub_path, 'r') as sub_file:
        sub_data = sub_file.read()

    for key, org_entry in org_dict.items():
        alpha_sub_copy = copy.deepcopy(sub_data)
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
"""

def process_folder(dir_path, superfolder, runall = True):
    # Grab all of the orgs in a folder and prep them for alpha runs.
    subprocess.call("mv arch_bak archive", shell=True, cwd=dir_path)
    for folder in os.scandir(dir_path):
        if folder.is_dir() and folder.name == "archive":
            org_dict = read_orgs("{}/archive".format(dir_path))
            
    # Make a folder to house all of the relevant files.
    run_name = "{}_alpharun".format(dir_path.split('/').pop())
    subprocess.call("mkdir -p {}".format(run_name), shell = True, cwd = dir_path)
    """make_env_files(org_dict, "/home/josh/flattest/BM4alpha/BM4alpha_init/environment.cfg")
    make_event_files(org_dict, "/home/josh/Link to MappingPeaks/Reference files/verif/2CompeteAB/2p5_alphas_events_AB.cfg",
                     "../{}/{}".format(superfolder, run_name))
    """
    for key, org in org_dict.items():
        subprocess.call("mkdir -p {}/archive".format(org['newname']), shell=True,
                        cwd = "{}/{}".format(dir_path,run_name))
        subprocess.call("cp {} {}/archive".format(org['file_handle'].path, org['newname']),
                        shell = True, cwd = "{}/{}".format(dir_path,run_name))
    subprocess.call("mv archive arch_bak".format(dir_path), shell = True, cwd = dir_path)
    newest_name = newest_org(org_dict)['newname']
    subprocess.call("cp -r ./{}/{}/archive .".format(run_name, newest_name),
                    shell = True, cwd = dir_path)


if __name__ == "__main__":
    for folder in os.scandir("/home/josh/archswap/archswap_ir"):
        if folder.is_dir() and "replicate" in folder.name:
            process_folder(folder.path, "{}".format(folder.name))
    print("AOT done!")
