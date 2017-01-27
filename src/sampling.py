import numpy
import distribution
from numpy.random import permutation
from emulator import reject
from distribution import normpdf

def lhcSampleSimp(dim, div = 10):
	"""
	Latin hypercube sampling from {1, 2, ..., div}^dim
	"""
	arr = []
	for i in range(dim):
		arr.append(permutation(range(div)).tolist())
	#take the transpose, 
	arr = zip(*arr)
	for i in range(len(arr)):
		arr[i] = list(arr[i])
	return arr

def uniRandSample(minx, maxx):
	"""
	Chooses a point uniformly at random from a box with corners minx and maxx (vectors)
	"""
	x = []
	for i in range(len(minx)):
		x.append(float(minx[i]) + float(maxx[i] - minx[i]) * numpy.random.random())
	return x

def lhcSample(dim, minx = [0], maxx = [1], div = 10):
	"""
	Return d points, chosen by latin hypercube method (d = div)
	"""
	indices = lhcSampleSimp(dim, div)
	points = []
	for i in range(div):
		minCorner = []
		maxCorner = []
		for j in range(dim):
			minCorner.append(minx[j] + (maxx[j] - minx[j]) * indices[i][j] / div)
			maxCorner.append(minx[j] + (maxx[j] - minx[j]) * (indices[i][j]+1) / div)
		points.append(uniRandSample(minCorner, maxCorner))
	return points

def sampleAround(k, x, dist = distribution.Distribution(normpdf([0.], [1.]))):
	"""
	samples k points from a distribution with spread described by dist, but centered at x
	"""
	newPoints = []
	for i in range(k):
		point = [sum(coord) for coord in zip([dist.sample()], x)]
		newPoints.append(point)
	return newPoints