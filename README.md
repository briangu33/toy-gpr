# toy-gpr

This is a proof-of-concept application of the Bayesian History Matching algorithm described by [Andrianakis et al.](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003968) to a toy problem. Uses Gaussian Process Regression to make predictions about the results of an expensive-to-run simulator, for the sake of simulator parameter optimization.

This project was implemented for the Institute for Disease Modeling during an internship under the mentorship of Daniel Klein (winter 2015-2016).

To run: run `python src/main.py`. Requires Python 2.7+, `numpy`, `scipy`, and `pyGPs` (can be installed via `pip`).
