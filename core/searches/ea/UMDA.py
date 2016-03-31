#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from operator import attrgetter
import numpy as np


class UMDA(object):
    def __init__(self, n_, pop_size, trunc_parameter):
        # Number of variables
        self.n = n_
        # Population size
        self.N = pop_size
        # Number of individuals in the selected population
        self.truncation = int(trunc_parameter * self.N)
        # Univariate vector initialized to 0.5
        self.univ_prob = 0.5*np.ones((self.n,self.n))  
        

    def generate(self, ind_init):
        # Generate N individuals and put them into the provided class
        
        # First, an empty,array fir population is created
        arz = []          
        for i in range(0,self.N):
          # A random permutation of size n is generated for each variable
          arz.append(np.random.permutation(range(1,self.n+1)))
        return list(map(ind_init, arz))
    
    def update(self, population):
        # Sort individuals so the best is first
        sorted_pop = sorted(population, key=attrgetter("fitness"), reverse=False)
        
        for i in range(self.n):
            # Compute the probabilistic vectors (frequency of values in each variable)
             self.univ_prob[i,:] = np.sum(np.asarray(sorted_pop[:self.truncation])==i,axis=0)/self.truncation
        # It is possible to visualize the probability vectors by uncommenting the following line  
        #print(self.univ_prob)  
