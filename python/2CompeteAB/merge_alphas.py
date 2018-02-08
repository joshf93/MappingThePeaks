"""Merge the bazillion alpha jobs into one job per replicate. Cuts down on job
submission, and since they run so quickly it should still be efficient."""

import os
import collections
import subprocess

target_dir = "/home/josh/flattest_cleanroom/final_run_alphas/sub_files"
out_dir = "{}/combined_alphas".format(target_dir)
subprocess.call("mkdir -p combined_alphas", shell = True, cwd = target_dir)

sub_dict = collections.defaultdict(list)
for sub in os.scandir(target_dir):
    if "alpha" in sub.name and ".sub" in sub.name:
        splitname = sub.name.split("_")
        repname = "{}_{}".format(splitname[0], splitname[1])
        sub_dict[repname].append(sub.path)

for repname, pathlist in sub_dict.items():
    pathlist.sort()

    datalist = []
    for path in pathlist:
        with open(path, 'r') as filehandle:
            datalist.append(filehandle.read())
    processed = []
    datalist.reverse()
    # Process the datalist. We need to keep the first set of #PBS, toss the rest
    processed.append(datalist.pop())

    for data in datalist:
        splitdata = data.split("\n")
        filtereddata = []
        for line in splitdata:
            if not line.startswith("#PBS") and not line.startswith("#!"):
                filtereddata.append(line)
        processed.append("\n".join(filtereddata))

    with open("{}/{}_combo_alpha.sub".format(out_dir, repname), 'w') as outfile:
        outfile.write("\n".join(processed))

sub_list = []
for file in os.scandir(out_dir):
    sub_list.append("qsub ./combined_alphas/{}".format(file.name))

with open("{}/sub_combo_alphas.sh".format(target_dir), 'w') as outfile:
    outfile.write("\n".join(sub_list))

subprocess.call("rm *.sub", shell=True, cwd=target_dir)
print('done')
    
