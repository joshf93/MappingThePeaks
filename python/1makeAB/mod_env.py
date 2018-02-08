"""handles modifying the environment file. Trivial if each task can only be
executed once and only has one copy of each task, but with multiple copies
so that the reward can be modified for subsequent performance of the same
task, it can get tricky."""

from collections import deque

def modify_environment(env_copy, org):
    # Split env_copy into lines
    # We could use normal lists and reverse them, but that's a bit
    # unintuitive. Dequeues are fine with leftpops.

    notused = "#THIS TASK WAS NOT USED BY THIS ORGANISM max_count=2"
    final_env = []
    env_list = deque(env_copy) # Lots of left popping.
    taskstr = deque(org[-1])
    
    # Echo is special. Handle it first.
    if taskstr[0] == "2":
        final_env.append(env_list[0])
    elif taskstr[0] == "1":
        final_env.append(env_list[0].replace("max_count=2", "max_count=1"))
    else:
        final_env.append(notused)
    taskstr.popleft() # Nuke echo for easier iteration
    env_list.popleft()

    #Handle all the regular cases
    for task in taskstr:
        if task == "0":
            env_list.popleft()
            env_list.popleft()
            final_env.append(notused)
            final_env.append(notused)
        elif task == "1":
            final_env.append(env_list.popleft())
            env_list.popleft()
            final_env.append(notused)
        elif task == "2":
            final_env.append(env_list.popleft())
            final_env.append(env_list.popleft())
        else:
            raise ValueError("Entry in taskstr wasn't 0, 1, or 2. \
Taskstr was: {}, org: {}".format(org[-1], org[0]))

    return(final_env)





if __name__ == "__main__":
    with open("/home/josh/Link to MappingPeaks/\
Reference files/verif/utilities/environment_modified.cfg") as envfile:
        env_data = envfile.read()

    org = ['replicate_1035.org',
           '1',
           '44761704.305267',
           '469',
           '95440.734126',
           '7', '94', '94', '92',
           '21202200000000002100000000210000000020000000000000200000000022021\
0000022000001']
    modify_environment(env_data.split("\n"), org)
    
