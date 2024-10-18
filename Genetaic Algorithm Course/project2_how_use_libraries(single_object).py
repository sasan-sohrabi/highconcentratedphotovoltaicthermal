"""
Problem Description:

    max z = 16*x1 + 22*x2 + 12*x3
    S.t.:
    5*x1 + 7*x2 + 4*x3 <= 10

"""
# Import relative libraries for solve project
import numpy as np
from geneticalgorithm import geneticalgorithm as ga


# Define the equations
def fitness_function(solution):
    x1 = solution[0]
    x2 = solution[1]
    x3 = solution[2]

    # Apply Constraints
    penalty = 0
    if 5 * x1 + 7 * x2 + 4 * x3 > 10:
        penalty = np.inf

    return -(16 * x1 + 22 * x2
             + 12 * x3) + penalty  # Negative the objective function for maximization and apply penalty


algorithm_parameters = {'max_num_iteration': None,
                        'population_size': 100,
                        'crossover_probability': 0.5,
                        'mutation_probability': 0.5,
                        'elit_ratio': 0.01,
                        'parents_portion': 0.3,
                        'crossover_type': 'uniform',
                        'max_iteration_without_improv': None}

# Create an instance of the Ga solver

model = ga(function=fitness_function, dimension=3, variable_type='bool', algorithm_parameters=algorithm_parameters)

model.run()
