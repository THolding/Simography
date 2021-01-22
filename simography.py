#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 20:21:52 2021
Simography - simulated demography based on marriage rules in populations
             structured by social kinship.
"""

import numpy as np;
import random;

import kinship_systems;
import marriage_rules;
import helpers;
from constants import (FEMALE, MALE,
                      FOCAL, MOTHER, FATHER, SISTER, BROTHER,
                      AUNT, UNCLE, COUSIN, UNRELATED);


#basically a container for data associated with individuals
class Agent:
    def __init__(self, gender, maternalLink=None, paternalLink=None, age=0):
        self.age = age; #in timesteps
        self.gender=gender;
        self.maternalLink = maternalLink; #reference to mother
        self.paternalLink = paternalLink; #reference to father
        self.spouseLink = None;
        self.marriageAge = None;
        self.offspringLinks = [];
        self.seekingSpouse = False;
        self.alive = True;
    
    def __str__(self):
        return "Age: {0}, Gender: {1}, has spouse: {2}, marriageAge: {3}, numOffspring: {4}, seekingSpouse: {5}".format(self.age, "Female" if self.gender==FEMALE else "Male", self.spouseLink is not None, self.marriageAge, len(self.offspringLinks), self.seekingSpouse);
        
    def apply_time_elapsed(self):
        self.age += 1;
        if self.spouseLink is not None:
            self.marriageAge += 1;

    
    def register_death_with_links(self):
        if self.spouseLink is not None:
            self.spouseLink.spouseLink = None;
        for offspring in self.offspringLinks:
            if self.gender==FEMALE:
                offspring.maternalLink=None;
            else:
                offspring.paternalLink=None;
        
        self.alive = False;
            

class Simography:
    def __init__(self):
        self.deceased = [];
        self.populationCarryingCapacity = 1000; #How large does the population need to be before mortality rate increases
        self.popBasedMortalityMultiplier = 0.0; #Set to 0 to turn carrying capacity offMultiplied the effect of population size induced mortality increases
    
    def set_kinship_system(self, kinship):
        self.kinshipSystem = kinship;
    
    def set_marriage_rules(self, marriage):
        self.marriageRules = marriage;
    
    def set_initial_population(self, population):
        self.population = population;
    
    #Set the age distributed rate of marriage (Females and Males)
    def set_marriage_rate(self, marriageRate):
        self.marriageRate = marriageRate;
    
    def set_reproduction_rate(self, reproductionRate):
        self.reproductionRate = reproductionRate;
    
    def set_mortality_rate(self, mortalityRate):
        self.mortalityRate = mortalityRate;
    
    def set_carrying_capacity_behaviour(self, multiplier, populationSizeThreshold):
        self.popBasedMortalityMultiplier = multiplier;
        self.populationCarryingCapacity = populationSizeThreshold;
        
    #Logic surrounding the death of agents. Tests for death using the agent's age and mortality rate
    #Returns true or false (true if individual fails the test and will die)
    def _death_test(self, age):
        if len(self.population) <= self.populationCarryingCapacity:
            return random.random() < self.mortalityRate[age];
        else: #Population is larger than 'carrying capacity' and mortality rate increases proportionally with
              #multiple of the carrying capacity
            multiplier = 1+((len(self.population) / self.populationCarryingCapacity) * self.popBasedMortalityMultiplier);
            return random.random() < (multiplier*self.mortalityRate[age]);
    
    def _register_marriage(self, agent1, agent2):
        if (agent1.spouseLink is not None) or (agent2.spouseLink is not None):
            raise ValueError("Cannot register marriage between agents if one or both already have spouses.");
        
        femaleAgent = agent1 if agent1.gender==FEMALE else agent2;
        maleAgent = agent1 if agent1.gender==MALE else agent2;
        
        femaleAgent.spouseLink = maleAgent;
        femaleAgent.marriageAge = 0;
        femaleAgent.seekingSpouse = False;
        maleAgent.spouseLink = femaleAgent;
        maleAgent.marriageAge = 0;
        maleAgent.seekingSpouse = False;
    
    #Set family links of a new born individual
    def _register_birth(self, newborn, mother, father):
        mother.offspringLinks.append(newborn);
        father.offspringLinks.append(newborn);
        newborn.maternalLink = mother;
        newborn.paternalLink = father;
        
    
    #Applies kinship and marriage rules to find the first suitable partner in potentialPartners
    def _find_valid_partner(self, focal, potentialPartners):
        for iother, other in enumerate(potentialPartners):
            marriageAllowed = self.marriageRules.marriage_allowed(focal, other, self.kinshipSystem);
            if marriageAllowed:
                return other, iother;
        
        #No suitable partners found, return None
        return None, None;
    
    
    def run(self, numTimeSteps, verbose=True, runName=""):
        #temporary data storage
        self.meanFertilityList = [];
        self.meanEligiblePartnersList = [];
        self.meanEligiblePartnersListIndex = [];
        self.numBirthsList = [];
        self.numDeathsList = [];
        self.runPrefix = runName+": " if runName != "" else "";
        
        for t in range(numTimeSteps):
            if verbose:
                print(self.runPrefix+"Starting time step: {0}  Population size: {1}".format(t, len(self.population)));
            #Somewhere to store new members of the population
            newAgents = [];
            
            #Randomly sort population
            random.shuffle(self.population); #In place. Removes any biases due to order.
            
            #Remove individuals who die
            agentsToKill = []; #add indiced to list then remove at end to avoid changing iteratee
            for i in range(0, len(self.population)):
                #test for death
                #Always remove individuals aged >= 200, since precomputed rates are only calculated up to this point
                if (self.population[i].age >= 200) or (self._death_test(self.population[i].age)):
                    agentsToKill.append(i);
                    self.population[i].register_death_with_links();
            #Move agents who have died from the population
            for i in agentsToKill[::-1]: #reverse order to avoid indices moving around
                self.deceased.append(self.population.pop(i));
            #self.population = [self.population[i] for i in range(0, len(self.population)) if i not in agentsToKill];
            if verbose:
                print("\t{0} agents died".format(len(agentsToKill)));
            self.numDeathsList.append(len(agentsToKill));
            
            
            #Find individuals looking for a marriage partner
            lookingForPartner = [];
            for agent in self.population:
                if agent.spouseLink is None:
                    if agent.seekingSpouse == True:
                        lookingForPartner.append(agent);
                    elif random.random() < self.marriageRate[agent.age]:
                        agent.seekingSpouse = True;
                        lookingForPartner.append(agent);
            if verbose:
                print("\t{0} agents seeking spouses".format(len(lookingForPartner)));
            
            #Create random marriage pairings
            marriageCount = 0;
            while len(lookingForPartner) > 0:
                focal = lookingForPartner.pop(0); #Remove from list because either a) a partner will be found and married, or b) no partners available this time step.
                partner, partnerIndex = self._find_valid_partner(focal, lookingForPartner);
                if partner is not None:
                    self._register_marriage(focal, partner);
                    marriageCount += 1;
                    del lookingForPartner[partnerIndex]; #Remove focal and partner from the search list
            if verbose:
                print("\t{0} marriages".format(marriageCount));
                    
            
            #Find individuals giving birth
            for agent in self.population:
                if agent.gender == FEMALE:
                    if (agent.marriageAge is not None) and (agent.spouseLink is not None): #only marriage females can give birth
                        #reproduction probability proportional to marriage age
                        if random.uniform(0, 1) < self.reproductionRate[agent.marriageAge]:
                            newBirth = Agent(random.choice((FEMALE, MALE)), age=0);
                            self._register_birth(newBirth, agent, agent.spouseLink);
                            newAgents.append(newBirth);
                    
            
            #Age population
            for agent in self.population:
                agent.apply_time_elapsed(); #ages agent and marriage
            
            #Add newly born members of the population to the main population
            self.population += newAgents;
            if verbose:
                print("\t{0} births".format(len(newAgents)));
            self.numBirthsList.append(len(newAgents));
            
            ####Store some data
            #Mean lifetime female fertility
            numOffspring = helpers.num_offspring_pf(self.deceased);
            meanFertility = np.mean(numOffspring);
            self.meanFertilityList.append(meanFertility);
            #Mean number of eligible marriage partners
            if t%5 == 0: #expensive calculation so only run once every 50 time steps
                meanEligiblePartners = helpers.mean_proportion_eligible_partners(self.population, self.marriageRules, self.kinshipSystem);
                self.meanEligiblePartnersList.append(meanEligiblePartners);
                self.meanEligiblePartnersListIndex.append(t);


