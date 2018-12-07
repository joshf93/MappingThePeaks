"""Curve fitting the alphas. Following:
https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html"""

from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import subprocess

# Initial fit used, changed after reivew to current method.
#def sof_fit(mu, alpha, beta):
#    return(sof_fit.w0 * np.exp((-alpha*mu) - (beta*(mu**2))))

def sof_fit(mu, alpha, beta):
    return(sof_fit.w0 * np.exp((-alpha*mu*beta))) 

#def sof_gamma_fit(mu, alpha, beta, gamma):
#    return(sof_fit.w0 * np.exp((-alpha*mu) - (beta*(mu**2) - (gamma*(mu**3)))))

def process_rep(pathpair, rep_name, output_directory, output_list):
    highfit = 0
    rep_list = []
    for filepath in pathpair:
        if "popA" in filepath:
            pop = "Fit"
        else:
            pop = "Flat"
            
        with open(filepath) as datafile:
            data = datafile.read()

        data = data.split("\n")
        
        mu = []
        finalfit = []
        sd = []
        initfit = []
        for line in data:
            if "mut" in line:
                continue # Bypass the header.
            splitline = line.split(',')
            mu.append(float(splitline[0]))
            finalfit.append(float(splitline[1]))
            sd.append(float(splitline[2]))
            initfit.append(float(splitline[4]))

        sof_fit.w0 = initfit[0]
        if initfit[0] > highfit:
            highfit = initfit[0]
            
        mu_arr = np.asarray(mu)
        ff_arr = np.asarray(finalfit)
        sd_arr = np.asarray(sd)

        #The first version uses the variance data to control the weight of the points,
        #But causes some weird fits, especially in the high variance spatial data
        #popt, pcov = curve_fit(f=sof_fit, xdata=mu_arr, ydata=ff_arr, sigma=sd_arr)
        popt, pcov = curve_fit(f=sof_fit, xdata=mu_arr, ydata=ff_arr)
        if pop == "Fit":
            col = 'b'
        else:
            col = 'r'
        plt.plot(mu_arr, ff_arr, '{}x'.format(col), label="Data {}".format(pop))
        plt.plot(mu_arr, sof_fit(mu_arr, *popt), '{}-'.format(col), label='Curve {}'.format(pop))
        plt.errorbar(mu_arr, finalfit, yerr=sd, ecolor = col, linestyle = "None")
        xcord = 0.25
        # Constraints on a and b mentioned by the supplementary info of SOF.
        c1 = bool(((popt[0]**2)/2) > popt[1])
        c2 = bool(popt[0] <= 1)
        if pop == "Fit":
             ycord = 0.85
             plt.annotate(s="{}: a={:.3f}, b={:.3f}, C1={}, C2={}".format("Fit", popt[0], popt[1], c1, c2),
                          xy=(xcord,ycord), xycoords = "figure fraction", size=10)
        else:
            ycord = 0.82
            plt.annotate(s="{}: a={:.3f}, b={:.3f}, C1={}, C2={}".format("Flat", popt[0], popt[1], c1, c2),
                         xy=(xcord,ycord), xycoords = "figure fraction", size=10)
        rep_list.append((rep_name, popt[0], popt[1], pop))
        #print(popt)
        #print("Initfit: {}".format(initfit[0]))
    
    plt.xlabel('Genomic Mutation Rate')
    plt.ylabel('Avg. Pop Fitness After 25 Generations')
    plt.xlim(0, 6.0)
    plt.ylim(0, highfit*1.1)
    plt.title(rep_name)
    plt.legend()
    #plt.show()
    plt.savefig("{}/{}_plot.png".format(output_directory, rep_name), dpi=400, bbox_inches="tight")
    plt.close()
    #print(popt)
    #print("Initfit: {}".format(initfit[0]))
    #print(type(ff_arr[0]))
    for item in rep_list:
        output_list.append(item)

if __name__ == "__main__":
    """process_rep(["/home/josh/flattest/minitests/BM4/BM4L77_highmut_comp_alphas/competition_data/alphafiles/replicate_9000_popA.dat",
                 "/home/josh/flattest/minitests/BM4/BM4L77_highmut_comp_alphas/competition_data/alphafiles/replicate_9000_popB.dat"],
                "replicate_9000", "/home/josh/flattest/minitests/BM4/BM4L77_highmut_comp_alphas/competition_data/alphafiles")"""
    
    target_dir = "/media/josh/3F416A910272CA4C/final_run_alphas/competition_data/alphafiles"
    output_dir = "/media/josh/3F416A910272CA4C/final_run_alphas/alpha_figs"

    subprocess.call("mkdir -p {}".format(output_dir), shell=True, cwd=target_dir)

    replicates = []
    for file in os.scandir(target_dir):
        if "replicate_" and ".dat" in file.name:
            strippedname = file.name.rstrip("_popA.dat")
            strippedname = strippedname.rstrip("_popB.dat")
            replicates.append(strippedname)
    repset = set(replicates)

    output_list = []
    for rep in repset:
        process_rep(("{}/{}_popA.dat".format(target_dir, rep),
                     "{}/{}_popB.dat".format(target_dir, rep)),
                    rep, output_dir, output_list)
    
    for idx, entry in enumerate(output_list):
        updatenum = int(entry[0].lstrip("replicate_"))
        entry = str(entry).rstrip(")").lstrip("(")
        entry.replace("'", "")
        entry.replace("'", "")
        output_list[idx] = "{},{}".format(entry, updatenum)

    
    output_list.sort()
    output_list.insert(0, "Name, alpha, beta, gamma, pop, update")
    with open("{}/alpha_ouput.csv".format(output_dir), 'w') as outfile:
        outfile.write("\n".join(output_list))
    
    print("Done!")
            
            
        
