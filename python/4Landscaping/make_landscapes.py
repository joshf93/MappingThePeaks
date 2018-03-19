# Run analyze on all of the AB organisms to get DFE info.

import sys
import os
import copy
import time
import subprocess


def make_landscape(org_dir, out_base, run_name):
    ref_path = "/home/josh/Link to MappingPeaks/Reference files/verif/4Landscaping/analyze_full_landscape.cfg"
    sub_path = "/home/josh/Link to MappingPeaks/Reference files/verif/4Landscaping/sub_org_landscape.sub"

    out_path = out_base.format(run_name)
    env_path = org_dir.replace("dominant", "environment_files")
    hpcc_path = "../{}/".format(out_path.split("/")[-1])

    org_list = []

    for org in os.scandir(org_dir):
        org_list.append((org.path, org.name))


    analyze_ref = open(ref_path)
    analyze_ref_data = analyze_ref.read()
    analyze_ref.close()
    sub_ref = open(sub_path)
    sub_ref_data = sub_ref.read()
    sub_ref.close()
    cmd_list = []

    subprocess.call("mkdir {}".format(out_path), shell=True)
    subprocess.call("mkdir -p analyzecfg", shell=True, cwd=out_path)
    subprocess.call("mkdir -p data", shell=True, cwd=out_path)
    subprocess.call("mkdir -p subs", shell=True, cwd=out_path)
    subprocess.call("mkdir -p output", shell=True, cwd=out_path)
    subprocess.call("cp -r {} ./organisms".format(org_dir), shell=True, cwd=out_path)
    subprocess.call("cp -r {} .".format(env_path), shell=True, cwd=out_path)

    for org in org_list:
        analyze_copy = copy.deepcopy(analyze_ref_data)
        analyze_copy = analyze_copy.replace("TARGET_ORGANISM", hpcc_path+"organisms/"+org[1])
        analyze_copy = analyze_copy.replace("FULL1_NAME", org[1]+"_1step.dat")
        analyze_copy = analyze_copy.replace("FULL2_NAME", org[1]+"_2step.dat")
        analyze_copy = analyze_copy.replace("LANDSCAPE3_NAME", org[1]+"_3step.dat")
        analyze_copy = analyze_copy.replace("LANDSCAPE4_NAME", org[1]+"_4step.dat")
        analyze_copy = analyze_copy.replace("LANDSCAPE5_NAME", org[1]+"_5step.dat")
        analyze_copy = analyze_copy.replace("DETAIL_NAME", org[1]+"_detail.dat")
        analyze_out = open(out_path+"/analyzecfg/"+org[1]+"_analyze", 'w')
        analyze_out.write(analyze_copy)
        analyze_out.close()
        sub_copy = copy.deepcopy(sub_ref_data)
        sub_copy = sub_copy.replace("ENVY_FILY",hpcc_path+"environment_files/"+org[1].rstrip("_popA.org").rstrip("_popB.org")+"_env.cfg")
        sub_copy = sub_copy.replace("ANALYZY_FILY", hpcc_path+"analyzecfg/"+org[1]+"_analyze")
        sub_copy = sub_copy.replace("RUN_NAME", out_path.split("/")[-1])
        sub_out = open(out_path+"/subs/"+org[1]+"_sub", 'w')
        sub_out.write(sub_copy)
        sub_out.close()

    sub_list = []
    subprocess.call("cat *_sub > megasub.sub", shell=True, cwd="{}/subs".format(out_path))

    with open("{}/subs/megasub.sub".format(out_path)) as megasub:
        megasub_text = megasub.read()

    megasub_text = megasub_text.split("\n")
    for idx, line in enumerate(megasub_text):
        if idx > 15 and (line.startswith("#") or line.startswith("cd")):
            megasub_text[idx] = "&fmt=18" # Just a flag that the line needs to go.
    while "&fmt=18" in megasub_text:
        megasub_text.remove("&fmt=18")

    with open("{}/subs/megasub.sub".format(out_path), 'w') as megasub:
        megasub.write("\n".join(megasub_text))

if __name__ == "__main__":
    org_dir = "/home/josh/flattest_cleanroom/final_run_comp_BM0/organisms"
    run_name = "your_name_goes_here" 
    out_directory = "/home/josh/flattest_cleanroom/{}"

    make_landscape(org_dir, out_directory, run_name)
