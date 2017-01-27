import pyGPs
import math

epsvar = 0.001 #apparently if this is too high GPR fails

def sim(x, func):
	"""
	Given input x, returns a simulated output given a simulation function
	"""
	import time
	from numpy import random
	#for more complex (toy) examples, a separate noise function might be more appropriate
	#noise = random.normal(0., epsvar**0.5)
	noise = epsvar**0.5 * (random.randn())
	time.sleep(0.01)
	y = func(x) + noise
	print "Simulating at ", x, ", obtained ", y
	return y


