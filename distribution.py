import random 
import numpy as np

class Distribution:
	mean_gentxn = 10
	
	def binominal(n,p):
		return np.random.binominal(n,p,1)
