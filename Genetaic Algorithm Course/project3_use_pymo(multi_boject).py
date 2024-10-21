"""
Objectives:

1- min f1(x) = x1^2 + x2^2 + x2^2
2- max f2(x) = -(x1-1)^2 - (x2-4)^2 - (x3-3)^2

S.t.
 
1- g1(x): x1 + x2 - x3 <= 1
2- g2(x): 3 * x1 - x2 - x3 >= 4
3- -10 <= x1 <= 10
4- -10 <= x2 <= 10
5- -10 <= x3 <= 10

"""

# Import relevant libraries
import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.config import Config
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter


# Develop the class for define problem
class MyProblem(ElementwiseProblem):

    def __init__(self):
        super().__init__(n_var=3,
                         n_obj=2,
                         n_ieq_constr=2,
                         xl=np.array([-10, -10, -10]),
                         xu=np.array([10, 10, 10]))

    def _evaluate(self, x, out, *args, **kwargs):
        f1 = x[0] ** 2 + x[1] ** 2 + x[2] ** 2
        f2 = (x[0] - 1) ** 2 + (x[1] - 4) ** 2 + (x[2] - 3) ** 2

        g1 = x[0] + x[1] - x[2] - 1
        g2 = -3 * x[0] + x[1] + x[2] + 4

        out["F"] = [f1, f2]
        out["G"] = [g1, g2]


problem = MyProblem()

# Initializing the Algorithm
Config.warnings['not_compiled'] = False

algorithm = NSGA2(
    pop_size=50,
    n_offsprings=10,
    sampling=FloatRandomSampling(),
    crossover=SBX(prob=0.9, eta=20),
    mutation=PM(eta=25),
    eliminate_duplicates=True,

)

termination = get_termination("n_gen", 100)

#  Optimization Process
res = minimize(problem,
               algorithm,
               termination,
               seed=5,
               save_history=True,
               verbose=True,
               )

# Result and Visualization
X = res.X
print(X)
print("\n---------\n")
F = res.F
print(F)

plot = Scatter(title="Three Variables Solutions")
plot.add(F, color="red")
plot.show()

ideal_point = F.min(axis=0)
nadir_point = F.max(axis=0)

print("ideal point: ", ideal_point)
print("nadir point: ", nadir_point)

import matplotlib.pyplot as plt
plt.figure(figsize=(8,6))
plt.scatter(F[:, 0], F[:, 1], s=50, facecolor='none', edgecolors='green')
plt.scatter(ideal_point[0], ideal_point[1], facecolor='none', edgecolors='red', marker='*', s=100)
plt.scatter(nadir_point[0], nadir_point[1], facecolor='none', edgecolors='black', marker='p', s=100)
plt.title('Objective Space with Ideal and Nadir Points')
plot.show()

# Normalization to prepare for MCDM
nF = (F - ideal_point) / (nadir_point - ideal_point)
print("Normalize amount of F is : ", nF )

fl = nF.min(axis=0)
fu = nF.max(axis=0)

print(f"Scale f1: [{fl[0]},{fu[0]}]")
print(f"Scale f2: [{fl[1]},{fu[1]}]")

plt.figure(figsize=(8,6))
plt.scatter(nF[:, 0], nF[:, 1], s=50, facecolor='none', edgecolors='green')
plt.title('Normalize Objective Vector')
plot.show()

#Compromise Programming
from pymoo.decomposition.asf import ASF
decomp = ASF()

Weights = np.array([0.2, 0.8])
opt_index = decomp.do(nF, 1/Weights).argmin()
print(f"Best ASF: \n Opt_index = {opt_index} \n F = {F[opt_index]}")

plt.figure(figsize=(8,6))
plt.scatter(F[:, 0], F[:, 1], s=50, facecolor='none', edgecolors='green')
plt.scatter(F[opt_index, 0], F[opt_index,1], marker='x', color='red', s=100)
plt.show()

X_Optimum = X[opt_index, :]
print(X_Optimum)

