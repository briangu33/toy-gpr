import numpy
import math
import scipy
from objfunc import ObjFunc
from distribution import Distribution
from distribution import normpdf
from simulator import sim
from emulator import emulate
from emulator import reject
from sampling import lhcSample
from sampling import sampleAround

#specify the range
minx = [-5.]
maxx = [5.]

#specify the threshold we want outputs to be above
threshold = 0.2

#specify the minimum probability mass a point must have over the threshold to not be rejected
rejectionDensity = 0.05

#specify the objective function
simFunc = ObjFunc(normpdf([0.], [1.]))

#initialize the array of points for emulation (test points) and simulation (simPoints)
test = []
simPoints = []

#counts the number of waves
count = 0 

#the number of sample points we emulate at surrounding each non-rejected simulated point
emulationPointsPerSamplePoint = 20 

#specify the number of waves (if we termination condition is given), simulations per wave, simulations at each point
numberOfWaves = 10
simulationsPerWave = 10
simulationsAtEachPt = 1

#can be used alongside a termination condition to stop the process at a certain wave
keepGoing = True 

def runSimulations(inputs, waveNumber):
	"""
	Parameters: input points and the wave number
	Returns: a set of points corresponding to the inputs and the simulator runs at each input
	"""
	newSimPoints = []
	for i in range(len(inputs)):
		#print "Wave", waveNumber, ":", "simulating point", i
		for j in range(simulationsAtEachPt): 
			point = [[0],[0]]
			point[0] = inputs[i]
			point[1] = sim(point[0], simFunc)
			newSimPoints.append(point)
	return newSimPoints

def getEmulationPoints(inputs, prediction):
	"""
	Parameters: input points and the emulator's predictions for the value of the simulator at these imput points
	Returns: a set of non-rejected emulated points which can serve as a sample to draw simulations from
	"""
	test = []

	#set test to hold points sampled around each non-rejected simulated point
	for point in inputs:
		indexOfPoint = inputs.index(point)
		predictedMean = prediction[0][indexOfPoint][0]
		predictedVariance = prediction[1][indexOfPoint][0]

		if not reject(predictedMean, predictedVariance, threshold, rejectionDensity):
			newPoints = sampleAround(emulationPointsPerSamplePoint, point)
			for newPoint in newPoints:
				test.append(newPoint)
	test = sorted(test)

	#remove all points rejected by emulator from test
	testPredictions = emulate(simPoints, test, wantToPlot = False)
	newTest = []
	for point in test:
		indexOfPoint = test.index(point)
		predictedMean = testPredictions[0][indexOfPoint][0]
		predictedVariance = testPredictions[1][indexOfPoint][0]
		if not reject(predictedMean, predictedVariance, threshold, rejectionDensity):
			newTest.append(point)
	test = newTest

	#plot the non-rejected emulated values
	emulate(simPoints, newTest, wantToPlot = True)

	return test

#perform numberOfWaves iterations
while keepGoing and count < numberOfWaves:

	#inputPoints is a list of points we've already run the simulator on
	#newInputPoints is a list of points we simulate at this wave
	#simPoints is a list of inputPoints associated with their respective simulator outputs
	#newSimPoints is a list of newInputPoints associated with their respective simulator outputs
	newInputPoints = []
	newSimPoints = []

	#on the first iteration, use latin hypercube sampling
	if count == 0:
		inputPoints = []
		newInputPoints = lhcSample(1, minx, maxx, simulationsPerWave) #use Latin Hypercube Sampling to generate initial points for simulation
		for point in newInputPoints:
			inputPoints.append(point)
	#on subsequent iterations, draw samples from non-rejected emulated points from the previous round
	else:
		for i in range(simulationsPerWave):
			point = test[int(math.floor(len(test) * numpy.random.random()))]
			inputPoints.append(point)
			newInputPoints.append(point)
		
	#get simulated values
	newSimPoints = runSimulations(newInputPoints, count)
	for point in newSimPoints:
		simPoints.append(point)
	#get emulator predictions at either all simulated values, or just the previous wave of simulations
	#prediction = emulate(simPoints[-1*simulationsPerWave:], inputPoints[-1*simulationsPerWave:], wantToPlot = False)
	prediction = emulate(simPoints, inputPoints, wantToPlot = False)
	#get new points to emulate at and sample from (either from previous wave of simulations or from all simulations)
	#test = getEmulationPoints(inputPoints[-1*simulationsPerWave:], prediction)
	test = getEmulationPoints(inputPoints, prediction)

	count = count + 1
