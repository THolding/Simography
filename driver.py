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


popSize = 200; #Initial population size
integratedMarriageRate = 0.9; #proportion of individuals getting married over lifetime
meanMarriedFertility = 4.1; #lifetime female fertility (for married women)

#Set survival rate with age
#survivalRate = 1 - (1.0 / (1.0 + np.exp(-0.05*(np.arange(0, 200)-100))));
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

#Initialise population
individuals = [Agent(FEMALE, None, None, age=random.randint(0,60)) for i in range(int(popSize/2))];
individuals = individuals + [Agent(MALE, None, None, age=random.randint(0,60)) for i in range(int(popSize/2))];

#random.seed(1);
#Setup and run model
#set kinship system and marriage rules
model = Simography();
model.set_initial_population(individuals);
#model.set_kinship_system(kinship_systems.MinimalKinshipSystem);
#model.set_kinship_system(kinship_systems.EskimoKinshipSystem);
model.set_kinship_system(kinship_systems.HawaiianKinshipSystem);
model.set_marriage_rules(marriage_rules.MinimalMarriageRules);
model.set_mortality_rate(1.0-survivalRate);
model.set_marriage_rate(marriageRate);
model.set_reproduction_rate(reproductionRate);
model.set_carrying_capacity_behaviour(1, 300);
model.run(2000);


##################
#### Plotting ####
#mean fertility time series
# plt.figure();
# plt.plot(model.meanFertilityList);
# plt.xlabel("time step (e.g. year)");
# plt.ylabel("mean female lifetime fertility");
# #mean number of eligible partners
plt.figure();
plt.plot(model.meanEligiblePartnersListIndex, model.meanEligiblePartnersList);
plt.xlabel("time step (e.g. year)");
plt.ylabel("mean proportion of eligible partners");
# #births and deaths
# plt.figure();
# #plt.plot(model.numBirthsList, 'b', label="births");
# #plt.plot(model.numDeathsList, 'r', label="deaths");
# plt.plot(np.array(model.numBirthsList)/np.array(model.numDeathsList), 'k', label="births / deaths");
# plt.legend(loc=0);
# plt.xlabel("time step (e.g. year)");
# plt.ylabel("births divided by deaths");

#population pyramid
helpers.plot_pop_pyramid(model.population, nbins=20);



popSizes = [100, 200, 300, 400, 500, 750, 1000, 1500];
kinshipSystemDict = {"Minimal": kinship_systems.MinimalKinshipSystem,
                      "Eskimo": kinship_systems.EskimoKinshipSystem,
                      "Hawaiian": kinship_systems.HawaiianKinshipSystem
                      };
for kinshipSystem in ["Minimal", "Eskimo", "Hawaiian"]:
    for popSize in popSizes:
        
