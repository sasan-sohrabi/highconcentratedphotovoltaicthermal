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
from pymoo.docs import algorithms


# Develop the class for define problem
class MyProblem(ElementwiseProblem):

    def __init__(self):

        super().__init__(n_var = 3,
                         n_obj = 2,
                         n_ieq_constr = 2,
                         xl = np.array([-10, -10, -10]),
                         xu = np.array([10, 10, 10]))

    def _evaluate(self, x, out, *args, **kwargs):

        f1 = x[0]**2 + x[1]**2 + x[2]**2
        f2 = (x[0]-1)**2 + (x[1]-4)**2 + (x[2]-3)**2

        g1 = x[0] + x[1] - x[2] - 1
        g2 = -3 * x[0] + x[1] + x[2] - 4

        out["F"] = [f1, f2]
        out["G"] = [g1, g2]

problem = MyProblem()

# Initializing the Algorithm
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.config import Config


Config.warnings['not_compiled'] = False

algorithm = NSGA2(
    pop_size = 50,
    n_offsprings = 10,
    sampling = FloatRandomSampling(),
    crossover = SBX(prob = 0.9, eta = 20),
    mutation = PM(eta = 25),
    eliminate_duplicates = True,

)

from pymoo.termination import get_termination
termination = get_termination("n_gen", 100)

#  Optimization Process
from pymoo.optimize import minimize

res = minimize(problem,
               algorithm,
               termination,
               seed = 7,
               save_history=True,
               verbose=True,
               )

# Result and Visualization
X = res.X
print(X)
print("\n---------\n")
F = res.F
print(F)

from pymoo.visualization.scatter import Scatter
plot = Scatter(title = "Three Variables Solutions")
plot.add(F, color="red")
plot.show()

