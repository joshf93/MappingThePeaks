"""This module handles interconversions between updates and generations using
time.dat. It returns the nearest neighbor if the exact update isn't found."""

def open_timedat(filepath):
    """Returns a timedat file without the header and split by lines then
whitespaces."""
    with open(filepath) as timedat:
        timedat_raw = timedat.read()
    timedat_lines = timedat_raw.split("\n")

    for idx, line in enumerate(timedat_lines):
        if line.startswith("#"):
            timedat_lines[idx] = ""

    while "" in timedat_lines:
        timedat_lines.remove("")

    timedat_split = []
    for line in timedat_lines:
        timedat_split.append(line.split(" "))

    return(timedat_split)


def find_nearest_update(timedat, update):
    dist_list = []
    for entry in timedat:
        dist_list.append(abs(update-float(entry[0])))
    nearest_idx = dist_list.index(min(dist_list))
    
    return(timedat[nearest_idx][2])

    
def update_to_gen(filepath, update_list):
    timedat = open_timedat(filepath)

    generation_list = []
    for update in update_list:
        generation_list.append(find_nearest_update(timedat, update))

    return(generation_list)


if __name__ == "__main__":
    print(update_to_gen("/home/josh/flattest/ChangeMut/ChangeMut/replicate_1061/time.dat",
                  [0,1000,2000,3000,4000,5000,180000]))
