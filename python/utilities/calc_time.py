import datetime
import os

def process_file(filepath):
    """Processes a single file, extracting the time the submission took"""
    times = []
    day_names = ("Sun", "Mon", "Tue", "Wed", "Thr", "Fri", "Sat")
    with open(filepath, 'r') as file:
        for line in file:
            if line[0:3] in day_names:
                times.append(datetime.datetime.strptime(line.rstrip("\n"),
                                                        "%a %b %d %H:%M:%S %Z %Y"))
                if len(times) == 2:
                    break
    return((times[1]-times[0]).total_seconds()/3600)

def process_folder(folder):
    """Takes an HPCC output folder and returns the time deltas as a list"""
    time_list = []
    for file in os.scandir(folder):
        if "times" not in file.name:
            time_list.append(process_file(file.path))
    return(time_list)

if __name__ == "__main__":
    target_dir = "/home/josh/flattest_cleanroom/final_run_landscape/output"
    result = process_folder(target_dir)
    print("Maximum time taken was {}hrs".format(max(result)))
    result.sort()
    result.append("TimeTakenHrs")
    result.reverse()
    print(result)
    result_str = [str(x) for x in result]
    with open("{}/times.dat".format(target_dir), 'w') as outfile:
        outfile.write("\n".join(result_str))
