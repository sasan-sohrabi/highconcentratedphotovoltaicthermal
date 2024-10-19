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
        f2 = -(x[0]-1)**2 - (x[1]-4)**2 - (x[2]-3)**2

        g1 = x[0] + x[1] - x[2] - 1
        g2 = -3 * x[0] + x[1] + x[2] - 4

        out["F"] = [f1, f2]
        out["G"] = [g1, g2]

problem = MyProblem()