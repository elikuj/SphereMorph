import math
import numpy as np
import scipy.constants as const

k_b = 1.380649* (10**(-23))     # joules/kelvin (boltzman const)
h = 6.62607015*(10**(-34))      # J*sec (planck const)
h_bar = const.hbar

gamma = 400

# h_bar**2 * (2*math.pi/(10**(-9) * 852))**2/(133*1.66*10**(-27) * 1.381 * 10**(-23))

print(10*10**6 * h_bar / k_b)


