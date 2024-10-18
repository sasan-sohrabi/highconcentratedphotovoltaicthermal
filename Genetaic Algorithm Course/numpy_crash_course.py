import numpy as np

NP1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print("type of NP1 is: ",type(NP1))

NP2 = np.array([[1, 2, 3],
                [4, 5, 6]])
print(NP2.shape)

print(NP2[:,1:3])