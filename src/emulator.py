import pyGPs
import numpy
import time

"""
It's really important that the emulator gets coded in GPy! 
We would certainly like to handle more than 1 dimension at a time, and to have more control
over plotting and visualization.
"""

def emulate(training, test, wantToPlot = True, k = pyGPs.cov.RBF()):
	"""
	Given training data, predicts values of function at test.
	pyGPs can only handle 1D training and test data
	"""
	model = pyGPs.GPR()
	model.setPrior(kernel = k) 
	x = []
	y = []
	z = []
	print "emulating..."
	for point in training:
		x.append(point[0])
		y.append(point[1])
	for point in test:
		z.append(point[0])
	x = numpy.asarray(x)
	y = numpy.asarray(y)
	z = numpy.asarray(z)
	model.setData(x, y)
	model.optimize(x, y) 
	model.predict(z)
	if wantToPlot:
		model.plot() #pyGPs gives limited control over plotting
	prediction = model.predict(z)
	return prediction

def reject(predictedMean, predictedVariance, threshold, rejectionDensity):
	"""
	Determine whether or not to reject a point
	"""
	from distribution import Distribution
	from distribution import normpdf

	distributionAtPoint = Distribution(normpdf([predictedMean], [predictedVariance]))
	if distributionAtPoint.cdf(threshold, float("inf")) < rejectionDensity:
		return True
	return False



