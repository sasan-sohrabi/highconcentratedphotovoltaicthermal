""""
              Project 1: Maximize the profit of leather manufactures
 Maximize the profit of leather limited manufactures two type of belts the deluxe model and the regular model. Each
 type requires 1 sq yd of leather. A regular belt requires 1 hour of skilled labor, and a deluxe belt requires 2 hours.
 Each week, 40 sq yd of leather and 60 hours of skilled labor are available. Each regular belt contributes $3 to profit
 and each deluxe belt, $4. Formulate a mathematical model to maximize the profit.
"""

"""
First step: Understanding the problem
Variables:
x1 =  the number of deluxe belts produced per week.
x2 =  the number of regular belts produced per week.
Objective Function:
z = 4*x1 + 3*x2
Constrains:
a- Leather constraint:
x1 + x2 ≤ 40
b- Skilled labor constraint:
2*x1 + x2 ≤ 60
c- Non-negativity constraints:
x1, x2 ≥ 0
"""

# The libraries
import numpy as np
import random
import matplotlib.pyplot as plt


# Second step: Define the objective function and the constrains
# The objective function
def objective_function(x1, x2):
    return 4 * x1 + 3 * x2


# The constrains
def constrains1(x1, x2):
    return x1 + x2 <= 40


def constrains2(x1, x2):
    return 2 * x1 + x2 <= 60


# Developing genetic algorithm
def genetic_algorithm(population_size, num_generation):
    # Third step: Initialization
    population = []
    fitness_history = []

    for i in range(population_size):
        x1 = random.uniform(0, 40)
        x2 = random.uniform(0, 60)
        population.append((x1, x2))

    best_solution = None
    best_fitness = float('-inf')

    for generation in range(num_generation):

        # Fourth step: Evaluation
        fitness = [objective_function(x1, x2) for x1, x2 in population]
        feasible_population = [individual for individual in population if
                               constrains1(individual[0], individual[1]) and constrains2(individual[0], individual[1])]

        # fifth step: Selection
        if feasible_population:
            feasible_fitness = [objective_function(x1, x2) for x1, x2 in feasible_population]
            parents = random.choices(feasible_population, weights=feasible_fitness, k=population_size)
        else:
            parents = []
            while len(parents) < population_size:
                potential_parnts = random.choice(population, weight=fitness)
                if constrains1(potential_parnts[0], potential_parnts[1]) and constrains2(potential_parnts[0],
                                                                                         potential_parnts[1]):
                    parents.append(potential_parnts)

        # Sixth step: Crossover
        offspring = []
        for i in range(population_size):
            parent1, parent2 = random.choices(parents, k=2)
            x1_child = random.uniform(min(parent1[0], parent2[0]), max(parent1[0], parent2[0]))
            x2_child = random.uniform(min(parent1[1], parent2[1]), max(parent1[1], parent2[1]))
            offspring.append((x1_child, x2_child))

        # Seventh step: Mutation
        mutation_rate = 1 / (generation + 1)  # Dynamic mutation rate
        for i in range(population_size):
            if random.random() < mutation_rate:
                offspring[i] = (random.uniform(0, 40), random.uniform(0, 60))

        # Eighth step: Elitism
        if best_solution is not None:
            offspring[0] = best_solution

        population = offspring

        # Ninth step: Find the best feasible solution
        feasible_solutions = [(x1, x2) for (x1, x2) in population if constrains1(x1, x2) and constrains2(x1, x2)]
        if feasible_solutions:
            best_solution = max(feasible_solutions, key=lambda x: objective_function(x[0], x[1]))
            best_fitness = objective_function(best_solution[0], best_solution[1])
        fitness_history.append(best_fitness)

        print(f"Generation{generation + 1}: Best solution = {best_solution}, Best fitness = {best_fitness}")

    plt.plot(range(1, num_generation + 1), fitness_history)
    plt.xlabel("Generation")
    plt.ylabel("Best fitness")
    plt.title("GA - Fitness Progress")
    plt.show()

    return best_solution, best_fitness

genetic_algorithm(20, 10)
