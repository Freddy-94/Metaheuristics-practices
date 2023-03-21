# Simulated Annealing Algorithm

## Description

Let $f : [0, \pi] ^n \to \mathbb{R}$ given by:

$$\begin{align}
        f(\mathbf{x}) = -\sum_{i=1}^n sin(x_{i})sin^{20}(i(\frac{x_{i}^{2}}{\pi})) 
\end{align}$$

This program implements the simulated annealing algorithm (https://en.wikipedia.org/wiki/Simulated_annealing) to approximate the global optimum of the given function f. In this implementation, we consider 5 different cooling functions, in order to study the behaviour of the algorithm with them, and compare the obtained results. The cooling functions implemented here were:

**1.   Linear cooling:**

$$ T_{k} = T_{k-1} - \beta $$

**2.   Geometric cooling:**

$$ T_{k} = \alpha * T_{k-1} $$

**3.   Logarithmic cooling:**

$$ T_{k} = \frac{ln(k)}{ln(k+1)} * T_{k-1} $$

**4.   Hybrid cooling:**

$$ T_{k} = \begin{cases} 
      (\frac{k}{k+1}) * T_{k-1} & k \leq β \\
      \alpha * T_{k-1} & k > β 
   \end{cases}
$$

**5.   Exponential cooling:**

$$ T_{k} = \frac{T_{k-1}}{1 + \beta T_{k-1}} $$

Although our algorithm is used in a function that takes real values in its domain variables, this same algorithm can be adjusted, so it can be used to found approximate solutions to the quadratic assignment problem (https://en.wikipedia.org/wiki/Quadratic_assignment_problem). Please take a look at: https://github.com/Freddy-94/Simulated-Annealing-Algorithm-Integer-Vars-Case to see how we found approximate solutions for problems of size 9!, 12!, 15!, and 30!. 


Our program consists of 3 different files:

1. CoolingFunctions.py
2. CoolFunList.py
3. annealingAlgo.py -> main program

Where the CoolingFunctions module provides a class for each one of the cooling function mentioned above, so each one of them can be used when necessary, in the main module, via polymorphism.

The CoolFunList module provides a way of creating a list of cooling function objets, and the annealingAlgo module implements the simulated annealing algorithm, as well as the cost function f described above.

Our program currently works for cost functions having a domain of the form: [a, b] x ... x [a, b], and it considers the cases of 2, 5, and 10 dimensions, although, in principle, it can be used in any dimension n passed. The iterations considered in the algorithm are of the form: 1000*dim, where dim is the dimension considered.

## Execution of the program

The program needs a configuration file that needs to be passed in the terminal. The data in this file consists on the parameters that the cooling functions need to be evaluated, and you can see an example of this file inside this project. Now, if for example, this config file is called "coolingFunctionsParams.txt", then, you only need to locate in the directory where the above modules, along with the mentioned config file is located, and run the command: 

           python annealingAlgo.py < coolingFunctionsParams.txt
 
## Relevant functions:

1. cost_function -> Cost function above
2. random_start  -> Generate a random initial solution 
3. random_neighbour   -> Generate a random "neighbour" solution
4. acceptance_probability -> Acceptance probability criteria
5. see_annealing -> Plot temperature, solutions, costs, vs. number iterations, respectively
6. annealing -> Simulated annealing algorithm

Example in 2 dimensions, with Linear cooling function:

![alt text](https://github.com/Freddy-94/Metaheuristics-practices/blob/main/SimulatedAnnealingLinearCoolingFunLastEpochTempGraph2dim.jpeg)
![alt text](https://github.com/Freddy-94/Metaheuristics-practices/blob/main/StatesvsCostsGraph2dim.png)
