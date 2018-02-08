# Analyze the results of competitions, including grouping replicates and
# plotting.

import sys
import os
import copy
import time
import subprocess
import collections
import pandas as pd
import random
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def grab_data(av_dir):
    fraction = pd.read_csv(av_dir, sep=' ', skiprows=18, index_col=False,\
                               usecols=[14])
    frac_series = fraction.iloc[:,0]
    # For *reasons* the fractions are out of 7. So 3.5 is really 0.5.
    # This changes it to the expected form.
    frac_series /= 7 
    
    fitness = pd.read_csv(av_dir, sep=' ', skiprows=18, index_col=False,\
                               usecols=[3])
    fit_series = fitness.iloc[:,0]
    
    generation = pd.read_csv(av_dir, sep=' ', skiprows=18, index_col=False,\
                               usecols=[12])
    gen_series = generation.iloc[:,0]

    return([frac_series, fit_series, gen_series])

def shows_sof(data, threshold):
    if max(data[0]) >= threshold:
        return(True)
    else:
        return(False)

def save_sof_list(sof_list, output_directory):
    line_list = []
    with open("{}/sof_list.csv".format(output_directory), 'w') as outfile:
        for item in sof_list:
            line_list.append("{},{},{}".format(item[0], item[1], item[2]))
        line_list.sort()
        outfile.write("\n".join(line_list))

    
plot_fitness = False
target_directory = "/media/josh/3F416A910272CA4C/flattest_cleanroom/final_run_comp_BM0/competition_data"
output_directory = "/media/josh/3F416A910272CA4C/flattest_cleanroom/final_run_comp_BM0/final_run_BM0_figs"
color_dict = {'0_r':("black", "black"),
              '0.5':("purple","violet"),
              '1.0':("blue","indigo"),
              "1.5":("green","lime"),
              "2.0":("yellow","gold"),
              "2.5":("orange","darkorange"),
              "3.0":("red","crimson"),
              "4.0":("brown","brown"),
              "4.5":("grey","darkslategrey"),
              "5.0":("black","darkslategrey")}

""" Crawl through the folders and sort the file locations into a dict of populations containing a dict of
mutation rates containing lists of reps:

population_dict[population][mut_rate][0,1,2...]"""

population_dict = collections.defaultdict(dict)

for folder in os.scandir(target_directory):
    
    if (not(folder.name[0:14] in population_dict)) or (not(folder.name[15:18] in population_dict[folder.name[0:14]])):
        population_dict[folder.name[0:14]][folder.name[15:18]] = []
        
    population_dict[folder.name[0:14]][folder.name[15:18]].append(folder.path+"/average.dat")


#There's probably some clever way to do this but whatever.
a = mpatches.Patch(color = 'yellow', label = "2.0")
b = mpatches.Patch(color = 'green', label = "1.5")
d = mpatches.Patch(color = 'blue', label = "1.0")
f = mpatches.Patch(color = 'purple', label = "0.5")
g = mpatches.Patch(color = 'red', label = "3.0")
h = mpatches.Patch(color = 'orange', label = "2.5")
i = mpatches.Patch(color = 'black', label = "0.0")

sof_list = []
                                                                  
# Plot and save all the plots.
for pop_key in population_dict.keys():
    # Build and nuke the plot each time because apparently garbage collection doesn't work properly for matplotlib plots
    title = "Random in Neighborhood Competition Results, {}".format(pop_key)

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.set_xlabel("Generations")
    ax1.set_ylabel("Fraction Flat")
    ax1.set_title(title)        

    plt.legend(handles=[g,h,a,b,d,f, i])
            
    for rate_key in population_dict[pop_key]:
        frac_color = color_dict[rate_key][0]
        fit_color = color_dict[rate_key][1]

        # Do SOF verification
        shows_sof_count = 0
        
        for rep in population_dict[pop_key][rate_key]:
            data = grab_data(rep)
            ax1.plot(data[2], data[0], color = frac_color)
            ax1.set_ylim([0,1])
            if plot_fitness:
                ax2.plot(data[2], data[1], color = fit_color, lw = 5)

            if shows_sof(data, 0.95):
                shows_sof_count += 1

        if shows_sof_count >= 3:
            if rate_key == '0_r':
                ed_rate_key = '0.0'
            else:
                ed_rate_key = rate_key
            tup = (pop_key, True, ed_rate_key)
        else:
            if rate_key == '0_r':
                ed_rate_key = '0.0'
            else:
                ed_rate_key = rate_key
            tup = (pop_key, False, ed_rate_key)
        sof_list.append(tup)
    
    "{}/{}_plot.png".format(output_directory, pop_key)
    plt.savefig("{}/{}_plot.png".format(output_directory, pop_key), dpi=400, bbox_inches="tight")
    plt.close(fig)

        
        
save_sof_list(sof_list, output_directory)
print("Done!")





