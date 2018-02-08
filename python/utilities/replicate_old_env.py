"""Takes environment.cfg and duplicates the tasks in such a way as to replicate
the 1.5x, 1.1x + 0 behavior of the original SOF paper."""

def most_rxns(line, val1, val2, lst):
    lst.append(line)
    tline = line.replace("max_count=1", "min_count=1:max_count=2")
    tline = tline.replace("value={}".format(val1), "value={}".format(val2))
    lst.append(tline)

with open("/home/josh/flattest/exactmultfit/environment.cfg") as env_file:
    env_data = env_file.read()

new_env = []
for line in env_data.split("\n"):
    if "REACTION ECHO" in line: # 1.05x, 1.05x
        new_env.append(line.replace("max_count=1", "max_count=2"))
    elif "REACTION  NOT" in line: # 1.1x, 1.05x
        most_rxns(line, 1.1, 1.05, new_env)
    elif "REACTION  NAND" in line: #1.15, 1.1
        most_rxns(line, 1.15, 1.1, new_env)
    elif "REACTION AND" in line: # named so we don't match against nand, andn
        most_rxns(line, 1.2, 1.1, new_env)
    elif "REACTION ORN" in line: #1.2, 1.1
        most_rxns(line, 1.2, 1.1, new_env)
    elif "REACTION  OR   or" in line: #1.25, 1.1
        most_rxns(line, 1.25, 1.1, new_env)
    elif "REACTION  ANDN" in line: #1.25, 1.1
        most_rxns(line, 1.25, 1.1, new_env)
    elif "REACTION  NOR" in line:
        most_rxns(line, 1.3, 1.1, new_env)
    elif "REACTION  XOR" in line:
        most_rxns(line, 1.5, 1.1, new_env)
    elif "REACTION  EQU" in line:
        most_rxns(line, 1.5, 1.1, new_env)
    else:
        most_rxns(line, 1.5, 1.1, new_env)
        
with open("environment_modified.cfg", 'w') as env_out:
    env_out.write("\n".join(new_env))
print("Done!")
