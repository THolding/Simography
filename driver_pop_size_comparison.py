#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 22:57:55 2021

@author: verwirrt
"""

import matplotlib.pyplot as plt;
import scipy.stats as stats;
import numpy as np;
import random;

from simography import Simography, Agent;
import kinship_systems;
import marriage_rules;
import helpers;
from constants import (FEMALE, MALE);


integratedMarriageRate = 0.9; #proportion of individuals getting married over lifetime
meanMarriedFertility = 4.1; #lifetime female fertility (for married women)

#Set survival rate with age
survivalRate = np.exp(-0.0004*np.arange(0,200));
cumulativeSurvivalRate = np.cumproduct(survivalRate);
#plt.figure(); plt.plot(cumulativeSurvivalRate);

#Set marriage rate with age
marriageRate = helpers.normaliseTo1(stats.norm.pdf(range(0, 200), loc=24, scale=4)) * integratedMarriageRate;
#plt.figure(); plt.plot(marriageRate);

#Set reproduction rate distribution. Years since first married
reproductionRate = helpers.normaliseTo1(stats.norm.pdf(range(0, 200), loc=1, scale=3)) * meanMarriedFertility;
#plt.figure(); plt.plot(reproductionRate);
#plt.figure(); plt.plot(np.cumsum(reproductionRate));

numReps = 10;
popSizes = [100, 200, 300, 400, 500, 750, 1000];
kinshipSystemDict = {"Minimal": kinship_systems.MinimalKinshipSystem,
                      "Eskimo": kinship_systems.EskimoKinshipSystem,
                      "Hawaiian": kinship_systems.HawaiianKinshipSystem
                      };
finalPopSizeOutputs = {};
finalPopSizeSDOutputs = {};
finalPyramidOutputs = {};
for kinshipSystemName in ["Minimal", "Eskimo", "Hawaiian"]:
    finalPopSizeOutputs[kinshipSystemName] = [];
    finalPopSizeSDOutputs[kinshipSystemName] = [];
    finalPyramidOutputs[kinshipSystemName] = [];
    for popSize in popSizes:
        finalPopSizeReps = [];
        finalPopPyramidReps = [];
        for rep in range(numReps):
            print(kinshipSystemName, popSize, rep);
            individuals = [Agent(FEMALE, None, None, age=random.randint(0,40)) for i in range(int(popSize/2))];
            individuals = individuals + [Agent(MALE, None, None, age=random.randint(0,40)) for i in range(int(popSize/2))];

            model = Simography();
            model.set_initial_population(individuals);
            model.set_kinship_system(kinshipSystemDict[kinshipSystemName]);
            model.set_marriage_rules(marriage_rules.MinimalMarriageRules);
            model.set_mortality_rate(1.0-survivalRate);
            model.set_marriage_rate(marriageRate);
            model.set_reproduction_rate(reproductionRate);
            model.set_carrying_capacity_behaviour(1, 1000);
            model.run(2000, verbose=True, runName=kinshipSystemName+"_"+str(popSize)+"_r"+str(rep));
            
            print("final pop size:", len(model.population));
            finalPopSizeReps.append(len(model.population));
            finalPopPyramidReps.append(helpers.get_age_sex_bin_frequencies(model.population, nbins=20));
        
        finalPopSizeOutputs[kinshipSystemName].append(np.nanmean(finalPopSizeReps));
        finalPopSizeSDOutputs[kinshipSystemName].append(np.nanstd(finalPopSizeReps));
        
        meanPyramid = finalPopPyramidReps[0];
        for df in finalPopPyramidReps[1:]:
            meanPyramid["femaleFreqs"] += df["femaleFreqs"];
            meanPyramid["maleFreqs"] += df["maleFreqs"];
        meanPyramid["femaleFreqs"] = meanPyramid["femaleFreqs"] / numReps;
        meanPyramid["maleFreqs"] = meanPyramid["maleFreqs"] / numReps;
        finalPyramidOutputs[kinshipSystemName].append(meanPyramid);
        
        #helpers.plot_pop_pyramid(meanPyramid);


import matplotlib.pyplot as plt;
plt.ioff(0);
for name in kinshipSystemDict.keys():
    np.savetxt(finalPopSizeOutputs[name], "output/final_pop_size_"+name+".csv", sep=",");
    np.savetxt(finalPopSizeSDOutputs[name], "output/final_pop_size_sd_"+name+".csv", sep=",");
    for i, df in enumerate(finalPyramidOutputs[name]):
        helpers.plot_pop_pyramid(df, nbins=20);
        plt.savefig("output/pyramids/pop_pyramid_{0}_{1}.png".format(name, popSizes[i]));
        plt.close();
plt.ion();
plt.figure();
plt.plot(popSizes, finalPopSizeOutputs["Minimal"], label="minimal");
plt.plot(popSizes, finalPopSizeOutputs["Eskimo"], label="Eskimo");
plt.plot(popSizes, finalPopSizeOutputs["Hawaiian"], label="Hawaiian");
plt.xlabel("Initial population size (t=0)");
plt.ylabel("Final population size (t=2000)");
        