"""
Objectives:

1- max f1(x) = x1 + 3 * x2
2- max f2(x) = -3 * x1 + x2
2- max f3(x) = x1 - x2

S.t.

1- g1(x): 2 * x1 + x2 <= 8
2- g2(x): x1 + 2 * x2 <= 10
3- 0 <= x1 <= 4
4- 0 <= x2 <= 8

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
        super().__init__(n_var=2,
                         n_obj=3,
                         n_ieq_constr=2,
                         xl=np.array([0, 0]),
                         xu=np.array([4, 8]))

    def _evaluate(self, x, out, *args, **kwargs):
        f1 = x[0] + 3 *x[1]
        f2 = -3 * x[0] + x[1]
        f3 = x[0] - x[1]

        g1 = 2 * x[0] + x[1]  - 8
        g2 = x[0] + 2 * x[1]  - 10

        out["F"] = [f1, f2, f3]
        out["G"] = [g1, g2]


problem = MyProblem()

# Initializing the Algorithm
Config.warnings['not_compiled'] = False

algorithm = NSGA2(
    pop_size=100,
    n_offsprings=40,
    sampling=FloatRandomSampling(),
    crossover=SBX(prob=0.95, eta=20),
    mutation=PM(eta=20),
    eliminate_duplicates=True,

)

termination = get_termination("n_gen", 1000)

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

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(F[:, 0], F[:, 1], F[:, 2], s=50, c='green', marker='o')
ax.set_xlabel('Objective 1')
ax.set_ylabel('Objective 2')
ax.set_zlabel('Objective 3')
ax.set_title('3D Scatter Plot of Objectives')

# Normalization to prepare for MCDM
nF = (F - ideal_point) / (nadir_point - ideal_point)
print("Normalize amount of F is : ", nF )

fl = nF.min(axis=0)
fu = nF.max(axis=0)

print(f"Scale f1: [{fl[0]},{fu[0]}]")
print(f"Scale f2: [{fl[1]},{fu[1]}]")
print(f"Scale f3: [{fl[2]},{fu[2]}]")

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(nF[:, 0], nF[:, 1], nF[:, 2], s=50, c='green', marker='o')
plt.title('Normalize Objective Vector')
plot.show()

#Compromise Programming
from pymoo.decomposition.asf import ASF
decomp = ASF()

Weights = np.array([0.2, 0.6, 0.2])
opt_index = decomp.do(nF, 1/Weights).argmin()
print(f"Best ASF: \n Opt_index = {opt_index} \n F = {F[opt_index]}")


ax.scatter(F[opt_index, 0], F[opt_index, 1], F[opt_index, 2], s=50, c='red', marker='o')
plt.show()

