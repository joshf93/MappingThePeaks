"""This script takes our newly minted A and B organisms, then runs them at various
mutation rates for a little while, and see what the ave fitness ends up being.
Allows us to fit alpha and beta parameters, then predict the critical mutation
rates. Will also help us troubleshoot why SOF doesn't work sometimes."""

import os
from collections import defaultdict 
import subprocess
import statistics
import "../1makeAB/get_tasks.py" as get_tasks

target_dir = '/home/josh/flattest/l0alphas/l0alphas_alphas/competition_data'
org_folder = '/home/josh/flattest/l0alphas/l0alphas_alphas/organisms'

final_avg_lines = []
fit_dict = {}
for folder in os.scandir(target_dir):
    if folder.is_dir() and "alphas" in folder.name:
        split_name = folder.name.split("_")
        rep_name = "{}_{}_{}".format(split_name[0], split_name[1], split_name[4])
        mut_rate = split_name[2]

        with open("{}/average.dat".format(folder.path)) as avgfile:
            avgfile_data = avgfile.read()

        # Grab the initial fitness
        with open("{}/{}.org".format(org_folder, rep_name)) as org_file:
                            for line in org_file:
                                if "Fitness.." in line:
                                    line_split = line.split()
                                    fitness = line_split[2]
                                    fit_dict[rep_name] = fitness
                                    break
        avglines = avgfile_data.split('\n')
        while "" in avglines:
            avglines.remove("")
        modline = "{} {} {} {}".format(avglines[-1], rep_name, fitness, mut_rate)
        final_avg_lines.append(modline)

with open("{}/merged_final_avg_raw.dat".format(target_dir), 'w') as outfile:
    outfile.write("\n".join(final_avg_lines))

# Do some processing here. We only care about the fitness ratio.
processed_avgs = defaultdict(lambda: defaultdict(list))
for line in final_avg_lines:
    splitline = line.split(" ")
    #ratio = float(splitline[3])/float(splitline[-2])
    processed_avgs[splitline[-3]][splitline[-1]].append(splitline[3])

subprocess.call("mkdir alphafiles", shell=True, cwd=target_dir)

for rep in processed_avgs:
    final_list = []
    #print(rep)
    for rate in processed_avgs[rep]:
        rmean = statistics.mean([float(num) for num in processed_avgs[rep][rate]])
        rdev = statistics.stdev([float(num) for num in processed_avgs[rep][rate]])
        if rdev == 0.0:
            rdev = 0.000001 # Give it a tiny value to avoid dying by zerodiv
        final_list.append("{},{},{},{},{}".format(rate, rmean, rdev, rdev/rmean, fit_dict[rep]))             
        final_list.sort()
    with open("{}/alphafiles/{}.dat".format(target_dir, rep), 'w') as outfile:
        final_list.insert(0, "mutrate,avgfit,stdev,cov,initfit")
        outfile.write("\n".join(final_list))

print("Done!")
