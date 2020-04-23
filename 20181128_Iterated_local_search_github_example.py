# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 15:53:48 2018
Version: 20181128

@author: 20304269
"""

#20181128_Iterated_local_search_github_example.py

import pandas as pd
import random
import copy

##INPUT (for batches of size 2)
df = pd.read_csv('small_example.csv', index_col=0, header=0)
df.columns = df.columns.astype(int) #to generate restart solution
o = df.columns.tolist() 

##INTIALISE [component 1]
initial_solution = [155,107,102,131,150,134] # Cost 17 
#Parameters for iterated local search
count_max = 5 #termination criterion
not_accepted_max = 3 #history criterion

#Cost function
def cost(solu):
    order_1 = solu[:int(len(solu)/2)]
    order_2 = solu[int(len(solu)/2):]
    comp = []
  
    for i,j in zip(order_1, order_2):
        comp.append(df.loc[i][j])
    cost = sum(comp)
    return cost

#Local search with two_opt swap (alternatives: insertion neighborhood) [component 2]
    #INSPIRATION - P. Diniz: http://pedrohfsd.com/2017/08/09/2opt-part1.html
    #!REQUIREMENTS! - same start and stop element (TSP)
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

#Perturbation with double bridge move (alternatives: random k opt move / number of swap or interchange moves) [component 3]
def perturbation(solu): 
    sliceLength = int(len(solu)/4)
    p1 = 1 + random.randrange(0,sliceLength) 
    p2 = p1 + 1 + random.randrange(0,sliceLength) #Combine first and fourth slice in order
    p3 = p2 + 1 + random.randrange(0,sliceLength) #Combine third and second slice in order          
    perturbation = solu[0:p1] + solu[p3:] + solu[p2:p3] + solu[p1:p2] #Return the combination of the above two combined slices
    return perturbation

#Acceptance criterion [component 4]
def acceptance_criterion(solu, test_solu, not_accepted):
    best_solu = solu
    if cost(test_solu) <= cost(solu):
        best_solu = copy.deepcopy(test_solu)
        not_accepted = 0
    else:
        best_solu = copy.deepcopy(solu)
        not_accepted += 1
    
    return best_solu, not_accepted

#Generate restart solution
def generate_restart_solution(o):
    restart_solution = random.sample(o, len(o)) 
    return restart_solution

##Iterated local search algorithm##     
def iterated_local_search(initial_solution, count_max, not_accepted_max):
    
    count = 0
    not_accepted = 0 
       
    #Step 1: Introduce an initial solution
    best_solution_ILS = initial_solution
    
    #Step2: Local search on initial solution
    solution = local_search(best_solution_ILS)       

    while not count == count_max:          
        
        #Step 3: Perturbation
        sol = perturbation(solution)
        #Step 4: Local search on perturbation
        test_sol = local_search(sol)
        
        #Step 5: Compare local search + local search on perturbation
        best_solu = acceptance_criterion(solution, test_sol, not_accepted)
        not_accepted = best_solu[1]
        
        #Step 6: Is acceptance criterion satisfied?
        if not_accepted <= not_accepted_max:
            solution = copy.deepcopy(best_solu[0])
            not_accepted = best_solu[1]            
            count += 1
    
        #Step 6b: Search history - Restart search if a number of iterations no improved solution is found
        else: 
            restart = generate_restart_solution(o)
            solution = local_search(restart)
            not_accepted = 0
            count = 0
            
        #Step 7: Store best solution of ILS algorithm
        if cost(best_solu[0]) < cost(best_solution_ILS):
            best_solution_ILS = copy.deepcopy(best_solu[0])          
                 
    return best_solution_ILS

##OUTPUT (for batches of size 2)
print('Cost of initial solution:', cost(initial_solution))               
orders = iterated_local_search(initial_solution, count_max, not_accepted_max)
print('Cost of best solution by batching each entry of Order_1 and Order_2:', cost(orders))


     


