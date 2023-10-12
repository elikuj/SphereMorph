import math
import numpy as np


eta = 10*math.pi*1.01/3
theta = math.pi/6

top = math.cos((eta-theta)/2)
bottom = math.sin((eta-theta)/2) 
print(1/math.sqrt(2) * top**2)


1/math.sqrt(2) * top**2

print(0.294 * 1/math.sqrt(2))

bott = 0.905*1/math.sqrt(2) - (0.294 * 1/math.sqrt(2))

print((0.0675-0.2079)*1/math.sqrt(2))

print(bott/math.sqrt(2) + (0.0675-0.2079)*1/math.sqrt(2))

