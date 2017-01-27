import math
import numpy
from scipy import integrate
from scipy.stats import norm

def normpdf(mean, var):
	"""
	Higher order function; returns a Gaussian with mean and variance
	"""
	def normpdfFunc(x):
		return math.exp((-1. * ((x[0] - mean[0]) ** 2)) / (2 * var[0])) / ((2. * math.pi * var[0]) ** 0.5)
	return normpdfFunc

#Untested
def normpdfNd(mean, var):
	"""
	Returns an N-D Gaussian with mean and variance list. Should be modified to allow for nontrivial
	covariance.
	"""
	def normpdfFuncNd(x):
		coeff = 1. / (2. * math.pi)
		for i in range(len(mean)):
			coeff /= (var[i]**2)
		exponent = 0
		for i in range(len(mean)):
			exponent += ((x[i] - mean[i])**2) / var[i]
		exponent *= -0.5
		return coeff * math.exp(exponent)
	return normpdfFuncNd

class Distribution:

	def __init__(self, pdf):
		self.pdf = pdf
		#pdf function ought to be vectorized

	def __call__(self, x):
		return self.pdf(x)

	def cdf(self, a, b):
		"""
		Returns the cdf of a 1D distribution evaluated from a to b
		Note that if the distribution is usually nearly 0 from a to b, this will return something
		unexpected and mathematically incorrect (0)
		"""
		def other(x):
			return self.pdf([x])
		return integrate.quad(other, a, b)[0]

	def invcdf(self, threshold, lo = -10., hi = 10., tolerance = 0.0001, depth=0):
		"""
		Returns the inverse cdf--the value v such that cdf(-inf, v) = threshold
		Note that due to the limitations of integrate.quad, we set lo and hi to small values at default 
		so that the standard N(0,1) can be handled appropriately
		This function calls cdf, which gives unexpected results when lo and hi are much wider than the
		relevant range. 
		"""
		mid = (lo + hi)/2.
		#note that because integrate.quad is not stable for the standard normal pdf, we use -99.
		#change this value if necessary
		error = self.cdf(-10, mid) - threshold
		if abs(error) < tolerance:
			return mid
		if error < 0:
			return self.invcdf(threshold, mid, hi, tolerance, depth+1)
		else:
			return self.invcdf(threshold, lo, mid, tolerance, depth+1)

	#NEED TO TEST
	def sample(self):
		"""
		Sample a point from a 1D distribution. Relies on invcdf, which has issues.
		"""
		r = numpy.random.random()
		return self.invcdf(r)
