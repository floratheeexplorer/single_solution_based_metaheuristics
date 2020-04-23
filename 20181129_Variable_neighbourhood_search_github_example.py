# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 15:53:48 2018
Version: 20181129

@author: 20304269
"""

#20181129_variable_neighbourhood_search_github_example.py

import pandas as pd
import random
import copy

#INPUT (for batches of 2)
df = pd.read_csv('small_example_extended.csv', index_col=0, header=0)
df.columns = df.columns.astype(int)
o = df.columns.tolist() 

##INTIALISE
#initial solution
initial_solution = [131,107,102,134,135,136,137,138,139,140,141,142]
#parameters
count_max = 10 #termination criterion
k_max = 3 #neighbourhood size

#0a: Cost function
def cost(solu):
    order_1 = solu[:int(len(solu)/2)]
    order_2 = solu[int(len(solu)/2):] 
    comp = []
  
    for i,j in zip(order_1, order_2):
        comp.append(df.loc[i][j])       
    cost = sum(comp)
    return cost

#0b: Cost component function - to define neighbourhood structures
def cost_component(solu): 
    order_1 = solu[:int(len(solu)/2)]
    order_2 = solu[int(len(solu)/2):]
    comp = []
    component = []
  
    for i,j in zip(order_1, order_2):
        comp.append(df.loc[i][j])
        component.append([i,j]) 
    s = pd.Series(comp).sort_values(ascending=False)
    sorted_index = s.index.tolist()
    
    return component, sorted_index

#0c: Defining the neighbourhood structure    
def neighbourhood_swap_first(solu): #neighbourhood that swaps the highest cost with the lowest (even)
    
    cost_comp = cost_component(solu)    
    component = cost_comp[0]
    sorted_index = cost_comp[1]
    
    #index of pair
    i1 = sorted_index[0]
    i2 = sorted_index[-1]
    a, b = solu.index(component[i1][1]), solu.index(component[i2][1])
    solu[a], solu[b] = solu[b], solu[a]    

    return solu

def neighbourhood_swap_second(solu): #neighbourhood that swaps the second highest cost with the lowest (even)
    
    cost_comp = cost_component(solu)    
    component = cost_comp[0]
    sorted_index = cost_comp[1]
    
    #index of pair
    i1 = sorted_index[1]
    i2 = sorted_index[-2]   
    a, b = solu.index(component[i1][1]), solu.index(component[i2][1])
    solu[a], solu[b] = solu[b], solu[a]
    
    return solu

def neighbourhood_swap_third(solu): #neighbourhood that swaps the third highest cost with the lowest (even)
    
    cost_comp = cost_component(solu)    
    component = cost_comp[0]
    sorted_index = cost_comp[1]
    
    #index of pair
    i1 = sorted_index[2]
    i2 = sorted_index[-3]
    
    a, b = solu.index(component[i1][1]), solu.index(component[i2][1])
    solu[a], solu[b] = solu[b], solu[a]
    
    return solu
    
#0d: Generate a random solution
def generate_random_solution(o):
    rdm_solution = random.sample(o, len(o)) 
    return rdm_solution

#Local search with two_opt swap (alternatives: insertion neighborhood) [component 2]
    #INSPIRATION - P. Diniz: http://pedrohfsd.com/2017/08/09/2opt-part1.html
    #!REQUIREMENTS! - same start and end element (TSP)
def local_search(solu): 
    solu = solu + [solu[0]]
    best = solu
    improved = True #first termination criterion
    iterations = 5  #second termination criterion to reduce runtime
    
    while improved:
        improved = False          
                       
        for i in range(1, iterations-2):
            for j in range(i+1, iterations):               
                if j-i == 1: #no changes, continue
                    continue                
                new_solution = solu[:]
                new_solution[i:j] = solu[j-1:i-1:-1] #two-opt swap
                if cost(new_solution) < cost(best):
                    best = copy.deepcopy(new_solution)
                    improved = True
        solu = best
        
    best = best[:-1]
    
    return best

##Variable neighbourhood search##
def variable_neighbourhood_search(initial_solution, count_max, k_max):           
    
    count = 0    
    best_solution = initial_solution  
        
    while not count == count_max: #stopping criterion is not satisfied    
    
        k = 0
        
        while k < k_max: #while in a defined neighbourhood            
         
            #Step1: Shaking (select a random solution s' in the neighbourghood of s)
            initial_random = generate_random_solution(o)           
            if k == 0:
                random_solution = neighbourhood_swap_first(initial_random)                
            elif k == 1:
                random_solution = neighbourhood_swap_second(initial_random)                
            elif k == 2:
                random_solution = neighbourhood_swap_third(initial_random)            
            
            #Step2: Local search on the solution
            test_solution = local_search(random_solution)
            
            #Step3: Move (is the solution s' in this neighbourhood better than the current best solution?)
            if cost(test_solution) < cost(best_solution): #yes, new best solution
                best_solution = copy.deepcopy(test_solution)
                k = 0
            
            else: #no, next neighbourhood
                k +=1
            
        count +=1 #termination counter  
    
    return best_solution       
                          
##OUTPUT: 
print('Cost of initial solution:', cost(initial_solution))                           
orders = variable_neighbourhood_search(initial_solution, count_max, k_max)
print('Cost after VNS:', cost(orders))  


