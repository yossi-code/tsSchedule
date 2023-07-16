import random
import numpy as np
import matplotlib.pyplot as plt
from TabuClasses import TSolutionInfo, Offer



# Define the objective function

def objective_function(x):
    return 2*x**4 - 5*x**2 + 4

fx = []
fy = []

# Define the neighborhood structure
def neighborhood(x, delta):
    return [x + delta, x - delta]

# Define the Tabu Search function
def tabu_search(delta, tabu_list_length, max_iterations):
    
    # Initialize the current solution
    current_solution = random.uniform(-5, 5)
    
    # Initialize the Tabu list
    tabu_list = []
    
    # Define the best solution so far
    best_solution = current_solution
    
    # Initialize the iteration counter
    iterations = 0
    
    # Start the Tabu Search algorithm
    while iterations < max_iterations:
        
        # Evaluate the objective function for the current solution
        current_objective = objective_function(current_solution)
        
        # Generate the candidate solutions
        candidate_solutions = neighborhood(current_solution, delta)
        
        # Evaluate the objective function for each candidate solution
        candidate_objectives = [objective_function(sol) for sol in candidate_solutions]
        
        # Choose the best candidate solution that is not in the Tabu list
        best_candidate = None
        best_candidate_objective = float('inf')
        for i in range(len(candidate_solutions)):
            if candidate_solutions[i] not in tabu_list and candidate_objectives[i] < best_candidate_objective:
                best_candidate = candidate_solutions[i]
                best_candidate_objective = candidate_objectives[i]
        
        # If all candidate solutions are in the Tabu list, choose the best one anyway
        if best_candidate is None:
            best_candidate = candidate_solutions[candidate_objectives.index(min(candidate_objectives))]
            best_candidate_objective = min(candidate_objectives)
        
        # Update the current solution
        current_solution = best_candidate
        print("Current solution value: ", current_solution)
        print("Current minimum value: ", objective_function(current_solution))
        print("Current Iteration", iterations)

        # Update the Tabu list
        tabu_list.append(current_solution)
        if len(tabu_list) > tabu_list_length:
            tabu_list.pop(0)
        
        # Update the best solution so far
        if best_candidate_objective < objective_function(best_solution):
            best_solution = best_candidate
        
        # Update the iteration counter
        iterations += 1
        fx.append(objective_function(current_solution))
        fy.append(current_solution)

    
    # Return the best solution found
    return best_solution

delta = 0.5
tabu_list_length = 10
max_iterations = 1000

best_solution = tabu_search(delta, tabu_list_length, max_iterations)

print("Best solution found:", best_solution)
print("Minimum value found:", objective_function(best_solution))

fig = np.linspace(-3,3,num=max_iterations)
plt.plot(fig,fx)
plt.plot(fig,fy)
plt.grid()
plt.axvline()
plt.axhline()
plt.show()
