#!/usr/bin/env python
import numpy as np
def projection(a,b):
#projection of vector a onto vector b
    return np.multiply((np.dot(a, b)/ np.linalg.norm(b)**2), b)
a = [1,2,3]
b = [1,3,7]

print(projection(a,b))
