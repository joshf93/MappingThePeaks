"""Parses dominant organisms for their info."""

import os

def task_count(task_str):
    """We can't just take the sum; the task_str number indicates
*how many* times each task was done; so it can be > 1. So we need
to count all the nonzero tasks."""
    counter = 0
    for task in task_str:
        if int(task):
            counter += 1
    return(counter)

def process(file_path):
    with open(file_path, 'r') as org_file:
        org_data = org_file.read()
    org_data = org_data.split("\n")

    #Variables
    viable = 0
    merit = 0
    gestation_time = 0
    fitness = 0
    errors = 0
    genome_size = 0
    copied_size = 0
    executed_size = 0

    for line in org_data:
            if line.startswith("# Is Viable"):
                viable = line.split()[-1]
                continue
            elif line.startswith("# Merit"):
                merit = line.split()[-1]
                continue
            elif line.startswith("# Gestation"):
                gestation_time = line.split()[-1]
                continue
            elif line.startswith("# Fitness"):
                fitness = line.split()[-1]
                continue
            elif line.startswith("# Errors"):
                errors = line.split()[-1]
                continue
            elif line.startswith("# Genome Size"):
                genome_size = line.split()[-1]
                continue
            elif line.startswith("# Copied Size"):
                copied_size = line.split()[-1]
                continue
            elif line.startswith("# Executed Size"):
                executed_size = line.split()[-1]
                continue

    #Now that we have those values, we can simplify the file.
    #Remove everything that comes before not and everything after
    #The last task.
    taskperf_line = org_data.index("# Tasks Performed:")
    del org_data[0:taskperf_line+1]
    task_list = []
    for line in org_data:
        if line.startswith("#"):
            line_splt = line.split(" ")
            task_list.append(line_splt[2])
    task_str = "".join(task_list)
    task_num = str(task_count(task_str))
    """"if len(task_str) > 77:
        print(task_str)
        print(file_path)"""
        #print("""WARNING: This task string is longer than it should be.
        #      This may indicate that you have a double-digit max_tasks,
        #      which are not currently supported.""")
        

    file_name = file_path.split("/")[-1]
    org_data = [file_name, viable, merit, gestation_time, fitness, errors,\
                        genome_size, copied_size, executed_size, task_str, task_num]

    return(org_data)

    """
    print("{}".format(file_path))
    print(org_data[0:10])
    print(taskperf_line)
    print(task_str)
    print(len(task_str))
    """
    

if __name__ == "__main__":
    process("/home/josh/flattest/\
l80eqval/l80eqval_init/replicate_3000/\
archive/replicate_3000.org")
