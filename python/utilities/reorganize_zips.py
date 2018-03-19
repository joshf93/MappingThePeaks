"""Converts a folder of zips to a single folder. Not a general tool;
it will only work properly for the specific format of the SOF zip folders."""

import sys, os, subprocess

targets = ["/home/josh/archswap/archswap_ir"]

for target_dir in targets:
    # Unzip all of the files.
    for zipfile in os.scandir(target_dir):
        if zipfile.is_file() and zipfile.path.endswith("zip"):
            print("Extracting {}.".format(zipfile.name))
            subprocess.call("unzip {}".format(zipfile.path), shell = True,\
                        cwd = target_dir)

    # Go through all of the subfolders and move the replicates back up.
    for folder in os.scandir(target_dir+"/mnt/local"):
        if folder.is_dir():
            for subfolder in os.scandir(folder.path):
                if subfolder.name == "popA" or subfolder.name == "popB":
                    for rep_folder in os.scandir(subfolder.path):
                        subprocess.call("mv replicate* {}".format(target_dir), shell = True,
                                cwd = subfolder.path)
                else:  
                    subprocess.call("mv replicate* {}".format(target_dir), shell = True,
                                cwd = folder.path)

    # Remove the temporary /mnt/ folder
    subprocess.call("rm -r mnt", shell = True, cwd = target_dir)
    # Remove all zips.
    subprocess.call("rm *.zip", shell = True, cwd = target_dir)

print("Done!")
