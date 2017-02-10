# toy-gpr

This is a proof-of-concept application of the Bayesian History Matching algorithm described by [Andrianakis et al.](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003968) to a toy problem. `toy-gpr` uses Gaussian Process Regression to make predictions about the results of an expensive-to-run simulator, for the sake of simulator hyperparameter optimization.

To run: run `python src/main.py`. Requires Python 2.7+, `numpy`, `scipy`, and `pyGPs` (can be installed via `pip`).

# History Matching

We are concerned with the behavior of a *simulator*, a model for some real-world process (for example, the spread of an epidemic) capable of making predictions. A simulator may have any number of hyperparameters whose optimal values are unknown. Oftentimes, however, we have historical datasets which we can use to help decide hyperparameters--our goal is therefore to *history match*.

Unfortunately, simulators are often computationally expensive to run in practice; it is impossible to run the simulator exhaustively at every point in the hyperparameter space. To get around this, we use a computationally inexpensive *emulator* to emulate the simulator. Given past simulator outputs, the emulator uses [Gaussian Process Regression](http://www.gaussianprocess.org/gpml/) to predict simulator output across hyperparameter space, allowing us to efficiently rule out large regions of implausible hyperparameter combinations. We iterate by running the simulator at points in the remaining plausible space, running the emulator across the remaining plausible space given simulator runs, and then further shrinking the plausible space. 

The algorithm can be summarized as follows:
1. Initialize the plausible region of hyperparameter space (for example, a high-dimensional box).
2. Sample a small number of points from the plausible region. Run the simulator at these points and record the output. It is helpful to make sure that the sampled points are reasonably spread out; for this implementation, we use a simple sampling procedure called [Latin Hypercube Sampling](https://en.wikipedia.org/wiki/Latin_hypercube_sampling).
3. Given the simulator outputs from the previous step, use the emulator to predict simulator output across all of the current plausible region. 
4. Using some history matching criterion, declare some of the current plausible region implausible if predicted simulator outputs are inappropriate. The size of the plausible region should shrink in this step.
5. Repeat steps 2 through 4 until some stopping criterion (fixed number of waves, plausible region does not shrink sufficiently, plausible region volume is under some threshold, etc.)

# Toy Problem

In our toy problem, we assume that there is only one relevant simulator hyperparameter *x*. The toy simulator output *f(x)* on any given run is determined by evaluating some simple user-specified underlying function *g(x)* (*g(x)* is chosen to be a bell curve in the graphs below--this has no special semantic meaning), and adding nosie *&epsilon;*. In practice, a simulator is meant to be a complex and computationally expensive approximation for an underlying process; this is not captured here, since the purpose of this program is simply to demonstrate the process of emulation. 

Given previous simulator outputs, the emulator uses GPR to give predictions (with both mean and variance) of simulator outputs across the hyperparameter space. A point in hyperparameter space is considered implausible if the emulator comes to believe that there is less than 5% probability of matching some history matching criterion. 

In this specific toy problem, the historical data we are trying to match is "outputs greater than 0.2". Thus, for *x* to be considered plausible, the emulator must believe that *P(f(x) > 0.2) > 0.05*.

Below, we show graphs of a sample run after waves 1, 2, 4, and 10 of simulations. The blue markers represent simulation results. The dark green line represents emulator predictions at points considered plausible. The shaded green region represents values within 2 standard deviations of the mean emulator predictions, again only at points considered plausible.

<img src="/imgs/wave1.png" alt="Wave 1" width="400px"> <img src="/imgs/wave2.png" alt="Wave 2" width="400px"> 
<img src="/imgs/wave4.png" alt="Wave 4" width="400px"> <img src="/imgs/wave10.png" alt="Wave 10" width="400px"> 

As the number of simulations increase, the mean emulator predictions gradually converge to the true noise-free process (a bell curve-shaped graph) generating simulator output. The green region also gradually shrinks to the "correct" area--for values of *x* between approximately -1.3 and 1.3, the simulator has approximately at least a 5% chance of outputting a value greater than 0.2.

# Known Issues

Sometimes, the entire hyperparameter space is marked as implausible in the first wave--this may be due to issues of numerical stability. pyGPs also seems to behave inconsistently across similar inputs.

# Acknowledgements 

This project was implemented for the Institute for Disease Modeling during an internship under the mentorship of Daniel Klein (winter 2015-2016).
