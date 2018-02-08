"""Find and replace"""

import os

folder_list = ["/home/josh/flattest_cleanroom/final_run_landscape_long/subs"]
subdir = ""
filename_key = "replicate"
target = "work_sltdel"
substitute = "work_sltdel_lethals"

for folder in folder_list:
    for file in os.scandir("{}/{}".format(folder, subdir)):
        if file.is_file() and filename_key in file.name:
            with open(file.path) as fileread:
                data = fileread.read()
            data = data.replace(target, substitute)
            with open(file.path, 'w') as filewrite:
                filewrite.write(data)

print("Done!")
                
                
