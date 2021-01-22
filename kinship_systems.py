#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 18:34:32 2021

@author: 
"""

from constants import (FEMALE, MALE,
                      FOCAL, MOTHER, FATHER, SISTER, BROTHER,
                      AUNT, UNCLE, COUSIN, UNRELATED);


#Considers all individuals unrelated
class MinimalKinshipSystem:
    def __init__(self):
        pass;
    
    @staticmethod
    def get_relation(focal, other):
        if other != focal:
            return UNRELATED;
        else:
            return FOCAL;


#See image in root folder for diagram
class EskimoKinshipSystem:
    def __init__(self):
        pass;
    
    @staticmethod
    #what is the relation of 'other' to 'focal'?
    def get_relation(focal, other):
        if other == focal:
            return FOCAL;
        
        if (other.maternalLink is None or other.paternalLink is None or
            focal.maternalLink is None or focal.maternalLink is None):
                return UNRELATED; #If they have no parents in the population, then they're unrelated
                                  #Only occurs in the initial population
        
        if other == focal.maternalLink:
            return MOTHER;
        
        if other == focal.paternalLink:
            return FATHER;
        
        if other in focal.maternalLink.offspringLinks:
            if other.gender == FEMALE:
                return SISTER;
            if other.gender == MALE:
                return BROTHER;
        
        #if 'other' is a sibling of my mother
        #or if 'other' is a sibling of my father
        if (focal.maternalLink in other.maternalLink.offspringLinks 
            or focal.paternalLink in other.maternalLink.offspringLinks):
                if other.gender==FEMALE:
                    return AUNT;
                if other.gender==MALE:
                    return UNCLE;
        
        #Relation of 'other' to focal is COUSIN if
        # 'other's mother is a sibling of my mother
        # or if 'other's father is a sibling of my mother
        # or if 'other's mother is a sibling of my father
        # or if 'other's father is a sibling of my father
        try:
            if focal.maternalLink in other.maternalLink.maternalLink.offspringLinks:
                return COUSIN;
        except: pass; #e.g. other has no maternal grandmother (artifact from initial conditions
        try:
            if focal.maternalLink in other.paternalLink.maternalLink.offspringLinks:
                return COUSIN;
        except: pass; #e.g. other has no paternal grandmother (artifact from initial conditions
        try:
            if focal.paternalLink in other.maternalLink.maternalLink.offspringLinks:
                return COUSIN;
        except: pass; #e.g. other has no maternal grandmother (artifact from initial conditions
        try:
            if focal.paternalLink in other.paternalLink.maternalLink.offspringLinks:
                return COUSIN;
        except: pass; #e.g. other has no paternal grandmother (artifact from initial conditions
        
        #All other cases mean the individuals are unrelated
        return UNRELATED;
            
#See image in root folder for diagram
class HawaiianKinshipSystem:
    def __init__(self):
        pass;
    
    @staticmethod
    #what is the relation of 'other' to 'focal'?
    def get_relation(focal, other):
        if other == focal:
            return FOCAL;
        
        if other == focal.maternalLink:
            return MOTHER;
        
        if other == focal.paternalLink:
            return FATHER;
        
        if other in focal.maternalLink.offspringLinks:
            if other.gender == FEMALE:
                return SISTER;
            if other.gender == MALE:
                return BROTHER;
        
        #if 'other' is a sibling of my mother
        #or if 'other' is a sibling of my father
        if (focal.maternalLink in other.maternalLink.offspringLinks 
            or focal.paternalLink in other.maternalLink.offspringLinks):
                if other.gender==FEMALE:
                    return MOTHER;
                if other.gender==MALE:
                    return FATHER;
        
        #Relation of 'other' to focal is COUSIN if
        # 'other's mother is a sibling of my mother
        # or if 'other's father is a sibling of my mother
        # or if 'other's mother is a sibling of my father
        # or if 'other's father is a sibling of my father
        try:
            if focal.maternalLink in other.maternalLink.maternalLink.offspringLinks:
                return SISTER if other.gender==FEMALE else BROTHER;
        except: pass; #e.g. other has no maternal grandmother (artifact from initial conditions
        try:
            if focal.maternalLink in other.paternalLink.maternalLink.offspringLinks:
                return SISTER if other.gender==FEMALE else BROTHER;
        except: pass; #e.g. other has no paternal grandmother (artifact from initial conditions
        try:
            if focal.paternalLink in other.maternalLink.maternalLink.offspringLinks:
                return SISTER if other.gender==FEMALE else BROTHER;
        except: pass; #e.g. other has no maternal grandmother (artifact from initial conditions
        try:
            if focal.paternalLink in other.paternalLink.maternalLink.offspringLinks:
                return SISTER if other.gender==FEMALE else BROTHER;
        except: pass; #e.g. other has no paternal grandmother (artifact from initial conditions
        
        #All other cases mean the individuals are unrelated
        return UNRELATED;
        