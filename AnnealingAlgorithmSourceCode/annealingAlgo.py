"""
Author: Alfredo Bernal Luna
Name: Simulated Annealing Algorithm Implementation
"""

import numpy as np
import math
import numpy.random as rn
import matplotlib.pyplot as plt  # to plot
import matplotlib as mpl
import sys
import copy
import CoolFunList
import CoolingFunctions 

def cost_function(n, x):
  sum = 0
  for i in range(1, n+1):
    sum += (math.sin(x[i-1])) * (math.sin(i*(x[i-1]**2/math.pi))**20)
  fun_value = -sum
  return fun_value
  
"""
Start of implementation of algorithm.
In our implementation, we must have a domain of the form: [a, b] x ... x [a, b], 
so that our algorithm works. 
"""

def random_start(n, interval):
    """ Generation of random point in the interval [a, b] x [a, b] x ... x [a,b],
        for some n \in N.
        limInf & limSup are the delimiting values that each variable can take;
        i.e., if the function has two real values, then, the domain of the 
        function will be [0, \pi] x [0, \pi]. Analogously, if the function has three
        real values, then, the domain of the function will be [0, \pi] x [0, \pi] x [0, \pi].
        This happen in general if n is the number of real variables that the function can
        take."""
    limInf, limSup = interval
    rand_start = limInf + (limSup - limInf) * rn.random((n,))
    return rand_start

def clip(x, interval):
    """Force each coordinate of the input vector, to be in its corresponding interval; i.e., 
        in this function the parameter 'x' is a scalar"""
    limInf, limSup = interval
    return max(min(x, limSup), limInf)

def random_neighbour(x, interval, fraction):
    """Move a little bit x, from the other coordinates."""
    rndm_neighbor_sol = []
    amplitude = (max(interval) - min(interval)) * fraction / 10.0 # size of the random step amplitude 
    for i in range(len(x)):  
        delta = (-amplitude/2.) + amplitude * rn.random()  # why delta is defined that way?
        rndm_neighbor_sol.append(clip(x[i] + delta, interval)) 
    return rndm_neighbor_sol

def acceptance_probability(cost, new_cost, temperature):
    if new_cost < cost:
        # print("    - Acceptance probabilty = 1 as new_cost = {} < cost = {}...".format(new_cost, cost))
        return 1
    else:
        try:
            p = np.exp(- (new_cost - cost) / temperature)
            # print("    - Acceptance probabilty = {:.3g}...".format(p))            
        except ZeroDivisionError:
            p = 0
        return p            

def see_annealing(coolFun, states, costs, temps):
    plt.figure()
    plt.suptitle(f"Evolution of states and costs of the simulated annealing - {coolFun.name} function")
    plt.subplot(121)
    plt.plot(states, 'r')
    plt.title("States")
    plt.subplot(122)
    plt.plot(costs, 'b')
    plt.title("Costs")
    plt.figure()
    plt.suptitle(f"Temperatures plot - {coolFun.name} function")
    plt.plot(temps, 'g')
    plt.title("Temps")
    plt.show()


def annealing(n,                              # Dimension of the domain of the function
              interval,                       # Interval of each of the variables in the domain
              random_start,                   # random_start function defined above
              cost_function,                  # cost_function defined above
              coolFunList,                    # List of cooling function objects without the atributes of last temp and iter (when apply)
              random_neighbour,               # random_neighbour function defined above 
              acceptance_probability,         # acceptance_probability function defined above              
              maxsteps=1000,                  # max number of iterations
              debug=True):
    """ Optimize the black-box function 'cost_function' with the simulated annealing algorithm."""    
    print("===============================================")
    print("Execution is starting. Please wait few mins ;)")
    print("===============================================")
    # state = random_start(n, interval) # If n=2, then, state is a random number in the set [0, \pi] x [0, \pi]
    # cost = cost_function(n, state) # First evaluation of the cost function, with a random solution  
    # print(f"The random initial solution fixed for all 5 cooling functions, and for each 10 executions is: {state}")       
    for i in range(1, 11):
        state = random_start(n, interval) # If n=2, then, state is a random number in the set [0, \pi] x [0, \pi]
        cost = cost_function(n, state) # First evaluation of the cost function, with a random solution
        state0 = copy.copy(state) # Save this state to replicate this same random value to all of the cooling functions
        for coolFun in coolFunList:
            T = coolFun.last_tmp
            T0 = copy.copy(T) # Save this temp to start new experiment
            states, costs, temps = [state], [cost], [] # store all of the found solutions, with their corresponding values, and the current temperature in the system   
            with open(f'{coolFun.name}Output{n}dimensions.txt', 'a') as f:
                f.write("============================================\n")
                f.write(f"           {coolFun.name}{n} dimensions    \n")
                f.write("============================================\n")
            for step in range(1, maxsteps+1):               
                fraction = step / float(maxsteps)
                if isinstance(coolFun, CoolingFunctions.LogarithmicCooling):
                    coolFun.iter = step+1 # This value is needed as per the behavior of the log function
                elif isinstance(coolFun, CoolingFunctions.HybridCooling):
                    coolFun.iter = step+2 # This value might change depending on the input parameter passed (beta)
                temps.append(T)
                new_state = list(random_neighbour(state, interval, fraction))
                new_cost = cost_function(n, new_state) 
                with open(f'{coolFun.name}Output{n}dimensions.txt', 'a+') as f:                    
                    content = "Step #{:>2}/{:>2} : T = {:>4.3f}, state = {}, cost = {:>4.3f}, new_state = {}, new_cost = {:>4.3f} ...\n".format(step, maxsteps, T, list(state), cost, new_state, new_cost)
                    #print("T value in iter " +  str(step) + " = " + str(T)) 
                    if debug: f.write(content)
                    if acceptance_probability(cost, new_cost, T) > rn.random():
                        state, cost = new_state, new_cost
                        states.append(state)
                        costs.append(cost)
                        # print("  ==> Accept it!")
                    # else:
                    #    print("  ==> Reject it...")
                    T = coolFun.cooling() # Decrease temperature
                    f.write("============================================\n")
                    f.write("                                            \n")
                    f.write("============================================\n")
            states = np.array(states)
            costs = np.array(costs)
            avg_solution = np.sum(costs)/costs.size # Solution evaluated in the objective function
            std_dev = math.sqrt((1/states.size)*(np.sum((states - avg_solution)**2)))
            min_sol = np.amin(costs)
            max_sol = np.amax(costs)
            with open(f'Statistical Results for dimension {n}.txt', 'a') as stats:
                stats.write("===========================================================================\n")
                # -stats.write(f"Current temperature for iteration {i}, for {coolFun.name} is: {temps[i-1]}\n")
                stats.write(f"Average solution for experiment {i}, for {coolFun.name} is: {avg_solution}\n")
                stats.write(f"Standard deviation for experiment {i}, for {coolFun.name} is: {std_dev}\n")
                stats.write(f"Min solution for experiment {i}, for {coolFun.name} is: {min_sol}\n")
                stats.write(f"Max solution for experiment {i}, for {coolFun.name} is: {max_sol}\n")
                stats.write("===========================================================================\n")
            coolFun.last_tmp = T0 # Start new experiment
            state = state0        # Start new experiment
            if i == 10:
                see_annealing(coolFun, states, costs, temps)
        # print(f"The random initial solution fixed for all 5 cooling functions, and for each 10 executions is: {state}")        
        #state = states[0]
        #cost = cost_function(n, state) # First evaluation of the cost function, with a random solution 
    print("======================================================")
    print("Success! Watch the output files in your directory :D")
    print("======================================================")
    
    return states, costs, temps # state, cost_function(n, state), states, costs, temps
        
def main():
    cool_funs = CoolFunList.CoolFunList()
    cool_fun = input().strip()
    while cool_fun != "":
        try:
            if cool_fun == "linear_cooling":
                name = cool_fun
                beta = float(input().strip())
                last_tmp = float(input().strip())
                cf = CoolingFunctions.LinearCooling(name, beta, last_tmp)

            elif cool_fun == "geometric_cooling":
                name = cool_fun
                alpha = float(input().strip())
                last_tmp = float(input().strip())
                cf = CoolingFunctions.GeometricCooling(name, alpha, last_tmp)

            elif cool_fun == "logarithmic_cooling":
                name = cool_fun
                itera = int(input().strip())
                last_tmp = float(input().strip())
                cf = CoolingFunctions.LogarithmicCooling(name, itera, last_tmp)

            elif cool_fun == "hybrid_cooling":
                name = cool_fun
                alpha = float(input().strip())
                beta = float(input().strip())
                itera = int(input().strip())
                last_tmp = float(input().strip())
                cf = CoolingFunctions.HybridCooling(name, alpha, beta, itera, last_tmp)

            elif cool_fun == "exponential_cooling":
                name = cool_fun
                beta = float(input().strip())
                last_tmp = float(input().strip())
                cf = CoolingFunctions.ExponentialCooling(name, beta, last_tmp)

            else:
                raise RuntimeError("Unknown Cooling function: " + cool_fun)

            cool_funs.append(cf)

            cool_fun = input().strip()
        except EOFError:
            break    
    #for coolfun in cool_funs:
    #    print(coolfun.last_tmp)
    list_dimensions = [2, 5, 10]
    for dim in list_dimensions:
        annealing(dim,                       # Dimension of the domain of the function
          (0, math.pi),                      # Interval of each of the variables in the domain
          random_start,                      # random_start function defined above
          cost_function,                     # cost_function defined above
          cool_funs,                         # List of cooling function objects without the atributes of last temp and iter (when apply)
          random_neighbour,                  # random_neighbour function defined above 
          acceptance_probability,            # acceptance_probability function defined above              
          maxsteps=1000*dim,                 # max number of iterations
          debug=True)
      
if __name__ == '__main__':
    main()
