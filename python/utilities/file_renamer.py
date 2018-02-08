"""Rename all files in a folder to .zip; used to fix an error I made one time.
could be useful for batch renaming of any kind though."""

import os, subprocess

target_dirs = ["/home/josh/archswap/archswap_AB/popA",
               "/home/josh/archswap/archswap_AB/popB"]

for dirs in target_dirs:
    for file in os.scandir(dirs):
        if file.is_file() and "replicate" in file.name and not ".zip" in file.name:
            subprocess.call("mv {} {}.zip".format(file.name, file.name), 
                            shell = True, cwd = dirs)

print("Done!")
