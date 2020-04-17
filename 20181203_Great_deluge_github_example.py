# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 09:28:40 2018

@author: 20304269
"""

#20181203_Great_deluge_small_example.py

import pandas as pd
import random
import copy

#INPUT (for batches of size 2)
df = pd.read_csv('small_example.csv', index_col=0, header=0)
df.columns = df.columns.astype(int) #to generate restart solution
o = df.columns.tolist() 

#Initialise a solution
sol = [155,107,102,131,150,134] # Cost 17 

#Calculate water-level - Cost
def cost(sol):
    order_1 = sol[:int(len(sol)/2)]
    order_2 = sol[int(len(sol)/2):]
    comp = []  
    for i,j in zip(order_1, order_2):
        comp.append(df.loc[i][j])       
    cost = sum(comp)
    return cost

#Generate neighbouring solution - Swap two orders
def neighbour(sol):
    idx = range(len(sol))
    i1, i2 = random.sample(idx, 2)
    sol[i1], sol[i2] = sol[i2], sol[i1]
    return sol

#Parameters
par = 2 #rain speed
count_max = 5 #termination criterion if no improvements
    
##Great deluge
    #INSPIRATION: My friend Charl!    
def greatdeluge(sol, par, count_max):

    solution = copy.deepcopy(sol)
    best_solution = copy.deepcopy(solution)
    initial_water_level = cost(solution)    

    i = 1 
    count = 0
    
    while i < 100:                  
        if count == count_max: 
            break
        
        else:            
            old_cost = copy.deepcopy(cost(solution))     
            new_solution = neighbour(solution) 
            new_cost = cost(new_solution) 
            if old_cost <= new_cost:
                count += 1 
                
            if new_cost < initial_water_level:
                count = 0
                solution = copy.deepcopy(new_solution)
                initial_water_level = initial_water_level - (initial_water_level - new_cost)/par
                if cost(solution) < cost(best_solution): #update best solution
                    best_solution = copy.deepcopy(solution)        
            i += 1

    return best_solution

##OUTPUT (for batches of size 2)
print('Cost of initial solution:', cost(sol))  
orders = greatdeluge(sol, par, count_max)
print('Cost of best solution by batching each entry of Order_1 and Order_2:', cost(orders))


    

