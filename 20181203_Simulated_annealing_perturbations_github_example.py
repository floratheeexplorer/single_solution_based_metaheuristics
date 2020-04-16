# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 13:24:32 2018

@author: 20304269
"""

#20181203_Simulated_annealing_small_example.py

import pandas as pd
import numpy as np
import random
import copy

#INPUT (for batches of size 2)
df = pd.read_csv('small_example.csv', index_col=0, header=0)
df.columns = df.columns.astype(int) #to generate restart solution
o = df.columns.tolist() 

#Initialise a solution
sol = [155,107,102,131,150,134] # Cost 17 

#Cost calculation
def cost(sol):
    order_1 = sol[:int(len(sol)/2)]
    order_2 = sol[int(len(sol)/2):]
    comp = []
  
    for i,j in zip(order_1, order_2):
        comp.append(df.loc[i][j])
    cost = sum(comp)
    return cost

#Generate a random neighbouring solution
def neighbour(sol):
    idx = range(len(sol))
    i1, i2 = random.sample(idx, 2)
    sol[i1], sol[i2] = sol[i2], sol[i1]
    return sol

#Acceptance probability    
def acceptance_probability(old_cost, new_cost, T):
    if new_cost < old_cost:
        return 1.0
    else:
        return np.exp((old_cost - new_cost) / T)

#Parameters (annealing schedule)
T_initial = 100.0 #temperature starting point
T_min = 0.0001 #temperature doesn't go below 0
alpha = 0.9 #temperature decreasing factor
accepted_max = 12 #max counter for accepted solutions
count_max = 3 #max counter for temperature stages without any acceptance

##Simulated annealing algorithm with cooling after a number of accepted perturbations:
    #Inspiration - K. E. Geltman: http://katrinaeg.com/simulated-annealing.html
def anneal(sol, T_initial, T_min, alpha, accepted_max, count_max):
    solution = copy.deepcopy(sol)
    best_solution = copy.deepcopy(solution)
    old_cost = cost(solution)
    
    T = T_initial 
    count = 0 
    accepted = 0 
    iterations = 100 #number of iterations of the algorithm
    i = 1 

    while i <= iterations:
        if T == T_min:
            break
        
        new_solution = neighbour(solution)
        new_cost = cost(new_solution)
        ap = acceptance_probability(old_cost, new_cost, T)
        if ap > random.random():
            count = 0
            accepted +=1
            solution = copy.deepcopy(new_solution)
            old_cost = copy.deepcopy(new_cost)            
            if cost(solution) < cost(best_solution): #update best solution
                best_solution = copy.deepcopy(solution)
        else: 
            accepted = 0
            count += 1
        
        if count == count_max: 
            break

        i += 1
        if accepted == accepted_max:
            accepted = 0
            T = T*alpha
            
    return best_solution

##OUTPUT (for batches of size 2)
print('Cost of initial solution:', cost(sol))               
orders = anneal(sol, T_initial, T_min, alpha, accepted_max, count_max)
print('Cost of best solution by batching each entry of Order_1 and Order_2:', cost(orders))

