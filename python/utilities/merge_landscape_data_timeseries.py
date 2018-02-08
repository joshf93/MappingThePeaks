import sys
import os
import copy
import time
import subprocess
import update_generations as ugen


def merge_landscape_data(target_dir, destination_dir):
    targets = ["1step.dat", "2step.dat", "3step.dat", "4step.dat", "5step.dat", "detail.dat"]
    output_filename = "{a}_{b}_{c}.dat".format(a=target_dir.split("/")[-2], b=target_dir.split("/")[-1], c="{}")
    

    for targ in targets:
        first = True
        out_list = []
        out_list.append("#The target_dir was: {}\n\
        #target_filename was: {}\n#output_filename was: {}\n".format(target_dir,
                                                                  targ,
                                                                  output_filename.format(targ)))
        # For including generation data.
        split_target = target_dir.split("/")
        #print(split_target)
        time_path = "{}/{}/{}/time.dat".format("/".join(split_target[0:5]), split_target[4], split_target[6])
        update_list = []
        header_len = 1
        for file in os.scandir(target_dir):
            if targ in file.name:
                with open(file.path) as targ_file:
                    targ_data = targ_file.read()
                    targ_data = targ_data.split("\n")
                    
                    if first:
                        for line in targ_data:
                            if line.startswith("#") or line.startswith("\n"):
                                out_list.append(line.rstrip("\n"))
                                header_len += 1
                        first = False
                    for line in targ_data:
                        # Grab header from first file, then skip it.
                        if not(line.startswith("#")) and not(line.startswith("\n")) and line:
                            mod_line = "{}{} {} {}".format(line.rstrip("\n"), target_dir.split("/")[-2],
                                                         file.name.split(".")[0], file.name.split(".")[0].split("_")[1].lstrip("0"))
                            try:
                                update_list.append(float(file.name.split(".")[0].split("_")[1].lstrip("0")))
                            except:
                                update_list.append(0)
                            out_list.append(mod_line)
        gen_list = ugen.update_to_gen(time_path, update_list)
        for idx, entry in enumerate(out_list):
            if entry.startswith("#"):
                continue
            #print("Idx is:{}, updatelist is: {}, genlist is:{}".format(idx, out_list[idx], gen_list[idx-header_len]))
            #input()
            out_list[idx] = "{} {}".format(entry, gen_list[idx-header_len])
        with open("{}/{}".format(destination_dir, output_filename.format(targ)), 'w') as of:
            of.write("\n".join(out_list))


if __name__ == "__main__":
    target_dirs = ["/home/josh/flattest_modern/BM1_min_landscape_ls"]
    destination_dir = "/home/josh/Link to MappingPeaks/BM1_min_landscape/data/dfe"

    for target in target_dirs:
        target_data = target+"/data"
        merge_landscape_data(target_data, destination_dir)
    print("Done!")
