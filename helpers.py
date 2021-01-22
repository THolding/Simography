#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 08:54:00 2021

@author: verwirrt
"""

import numpy as np;
import pandas as pd;
import matplotlib.pyplot as plt;
import random;
import pandas as pd;

from constants import FEMALE, MALE;

#Normalise an iteratable to sum to 1
def normaliseTo1(data):
    return data / sum(data);

#returns an array containing the number of offspring for each female in the population
def num_offspring_pf(population):
    numOffspring = np.array([len(agent.offspringLinks) for agent in population if agent.gender==FEMALE]);
    return numOffspring;

#Returns the proportion of eligible partners for an average non-married agent
#Ignores whether an agent or potential partner is seeking a spouse
#Windows/widowers are counted as 'married' as they do not remarry
def mean_proportion_eligible_partners(population, marriageRules, kinshipSystem):
    if len(population) > 5000: #Expensive in big populations, so sample 2000 random unmarried individuals instead
        subpop = random.sample(population, k=5000);
    else: #1000 or less unmarried individuals
        subpop = population;
    
    #Subset unmarried agents. Note using marriage age excludes widows/widowers
    unmarried = [agent for agent in subpop if agent.marriageAge is not None];
    numEligibleList = [];
    
    for focal in unmarried:
        numEligible = sum([marriageRules.marriage_allowed(focal, other, kinshipSystem) for other in unmarried]); #focal is discounted by kinship rules
        numEligibleList.append(numEligible);
    return np.sum(numEligibleList)/len(unmarried) / len(subpop);


def get_age_sex_bin_frequencies(population, nbins=20):
    femaleAges = np.array([agent.age for agent in population if agent.gender==FEMALE]);
    maleAges = np.array([agent.age for agent in population if agent.gender==MALE]);
    bins = np.linspace(0,200,nbins+1);
    binLabels = [str(int(bins[i]))+"-"+str(int(bins[i+1])) for i in range(0, len(bins)-1)];
    
    femaleBinLabels = np.digitize(femaleAges, bins=bins);
    binnedFemales = np.array([sum(femaleBinLabels==i) for i in range(1, len(bins+1))]);
    
    maleBinLabels = np.digitize(maleAges, bins=bins);
    binnedMales = np.array([sum(maleBinLabels==i) for i in range(1, len(bins+1))]);
    
    df = pd.DataFrame();
    df["ageCat"] = binLabels;
    df["femaleFreqs"] = binnedFemales;
    df["maleFreqs"] = binnedMales;
    return df;

def plot_pop_pyramid(population, nbins=20):
    # femaleAges = np.array([agent.age for agent in population if agent.gender==FEMALE]);
    # maleAges = np.array([agent.age for agent in population if agent.gender==MALE]);
    # bins = np.linspace(0,200,nbins+1);
    # binLabels = [str(int(bins[i]))+"-"+str(int(bins[i+1])) for i in range(0, len(bins)-1)];
    
    # femaleBinLabels = np.digitize(femaleAges, bins=bins);
    # binnedFemales = np.array([sum(femaleBinLabels==i) for i in range(1, len(bins+1))]);
    
    # maleBinLabels = np.digitize(maleAges, bins=bins);
    # binnedMales = np.array([sum(maleBinLabels==i) for i in range(1, len(bins+1))]);
    
    if isinstance(population, list):
        binnedData = get_age_sex_bin_frequencies(population, nbins);
    else: #assume dataframe data provided
        binnedData = population;
    
    plt.figure();
    plt.barh(binnedData["ageCat"], binnedData["femaleFreqs"], align="center", color="r", label="female");
    plt.barh(binnedData["ageCat"], -binnedData["maleFreqs"], align="center", color="b", label="male");
    plt.ylabel("Age category (time steps, e.g. years)");
    plt.legend(loc=0);
    plt.tight_layout();


#TODO: possible method: construct relatedness network with edges 0.25 for tree links, and 0.5 for siblings
#      Use network library to find path between each node.
#      Then multiply edge values in path to get relatedness. Repeat for each node.
def calc_mean_relatedness(focal, population):
    pass;





# df = pd.DataFrame({'Age': ['0-4','5-9','10-14','15-19','20-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79','80-84','85-89','90-94','95-99','100+'], 
#                    'Male': [-49228000, -61283000, -64391000, -52437000, -42955000, -44667000, -31570000, -23887000, -22390000, -20971000, -17685000, -15450000, -13932000, -11020000, -7611000, -4653000, -1952000, -625000, -116000, -14000, -1000], 
#                    'Female': [52367000, 64959000, 67161000, 55388000, 45448000, 47129000, 33436000, 26710000, 25627000, 23612000, 20075000, 16368000, 14220000, 10125000, 5984000, 3131000, 1151000, 312000, 49000, 4000, 0]})


# AgeClass = ['100+','95-99','90-94','85-89','80-84','75-79','70-74','65-69','60-64','55-59','50-54','45-49','40-44','35-39','30-34','25-29','20-24','15-19','10-14','5-9','0-4']

# bar_plot = sns.barplot(x='Male', y='Age', data=df, order=AgeClass)

# bar_plot = sns.barplot(x='Female', y='Age', data=df, order=AgeClass)

# bar_plot.set(xlabel="Population (hundreds of millions)", ylabel="Age-Group", title = "Population Pyramid")