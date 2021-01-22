#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 18:40:52 2021

"""

from constants import (FEMALE, MALE,
                      FOCAL, MOTHER, FATHER, SISTER, BROTHER,
                      AUNT, UNCLE, COUSIN, UNRELATED);


#Allows marriage / reproduction between any two individuals of the opposite sex
#Excludes individuals under 16
#Ignore kinship
class MinimalMarriageRules:
    def __init__(self):
        pass;
    
    @staticmethod
    def marriage_allowed(indiv1, indiv2, kinshipSystem):
        if (indiv1.gender == indiv2.gender) or (indiv1.age < 16) or (indiv2.age < 16):
            return False;
        
        #relation = kinshipSystem.get_relation(indiv1, indiv2); #indiv2's relation to focal (indiv1)
        return True;


#Minimum marriage age: 16
#Heterosexual marriage only
#No marriages to MOTHER, FATHER, SISTER or BROTHER
#No constraints on age difference
class DefaultMarriageRules:
    def __init__(self):
        pass;
    
    @staticmethod
    def marriage_allowed(indiv1, indiv2, kinshipSystem):
        if (indiv1.gender == indiv2.gender) or (indiv1.age < 16) or (indiv2.age < 16):
            return False;
        
        relation = kinshipSystem.get_relation(indiv1, indiv2); #indiv2's relation to focal (indiv1)
        if relation in (MOTHER, FATHER, SISTER, BROTHER):
            return False; #cannot marry these relations
        
        #everything else goes
        return True;
        