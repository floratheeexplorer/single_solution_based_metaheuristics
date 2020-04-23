# single_solution_based_metaheuristics
Four single-solution based metaheuristics are presented for small matrix examples, namely iterated local search, variable neighbourhood search and descent, simulated annealing and the great deluge. Information on each algorithm follows.

1. Iterated locat search '20181128_Iterated_local_search_github_example.py': 
example file: 'small_example.csv'

The components are a cost function being minimised for the combinatorial optimisation problem and a local search routine that guides from an initial solution to the bottom of the basin of attraction.

Literature: Lourenco HR, Martin OC and Stuetzle T, 2003, Iterated local search, pp. 320-353
            in Handbook of metaheuristics. Springer.
            Stuetzle T, 1998, Local search algorithms for combinatorial problems, Doctoral Dissertation,
            Darmstadt University of Technology.

2a. Variable neighbourhood search '20181129_Variable_neighbourhood_search_github_example.py':
example file: 'small_example_extended.csv'

It consists of the three steps shaking, local search and move in which it successively explores a set of predefined neighbourhood
structures to improve an initial solution.

2b. Variable neighbourhood descent '20181129_Variable_neighbourhood_decent_github_example.py':
example file: 'small_example_extended.csv'

The variable neighbourhood descent excludes the shaking step and is thus the deterministic version of the article.

Literature: Blum C and Roli A, 2003, Metaheuristics in combinatorial optimization: Overview and
            conceptual comparison, ACM computing surveys (CSUR), 35(3), pp. 268-308.
            Talbi EG, 2009, Metaheuristics: from design to implementation, John Wiley & Sons,
            New Jersey, United States.
            
3. Simulated annealing '20181203_Simulated_annealing_perturbations_github_example.py':
example file: 'small_example.csv'

The process of annealing is transposed to solving an optimisation problem. The objective function is minimised, similar to the energy of the material by controlling a fictitious temperature that is represented by a parameter.

Literature: Dreo J, Petrowski A, Siarry P and Taillard E, 2006, Metaheuristics for hard
            optimization: methods and case studies, Springer Science & Business Media, Berlin.
            Van Laarhoven PJ and Aarts EH, 1987, Simulated annealing, pp. 7-15 in Simulated
            annealing: Theory and applications. Springer.
            
4. Great deluge: '20181203_Great_deluge_github_example.py':
example file: 'small_example.csv'

The great deluge is a variant of simulated annealing. However, it accepts a solution according to the idea of a hiker who want to keep her feet try by visiting the peaks in the search space. The only parameter that needs to be calibrated is the rain speed.

Literature: Dueck G, 1993, New optimization heuristics, Journal of Computational physics, 104(1),
            pp. 86-92.







