

from . import GreedySolver
import numpy as np

class GreedyStochasticSolver(GreedySolver):
    _TEMPERATURE_DECAY_FACTOR = None
    _INITIAL_TEMPERATURE = None
    _N = None

    def __init__(self, roads, astar, scorer, initialTemperature, temperatureDecayFactor, topNumToConsider):
        super().__init__(roads, astar, scorer)

        self._INITIAL_TEMPERATURE = initialTemperature
        self._TEMPERATURE_DECAY_FACTOR = temperatureDecayFactor
        self._N = topNumToConsider

    def _getSuccessorsProbabilities(self, currState, successors):
        # Get the scores
        X = np.array([self._scorer.compute(currState, target) for target in successors])

        # Initialize an all-zeros vector for the distribution
        P = np.zeros((len(successors),))

        # TODO: Fill the distribution in P as explained in the instructions.
        XNorm = X / np.min(X)
        XBestNIndices = XNorm.argsort()[:self._N]

        sumDenom = np.sum(XNorm[XBestNIndices] ** (-1 / self.T))
        P[XBestNIndices] = (XNorm[XBestNIndices] ** (-1 / self.T)) / sumDenom

        # for index in XBestNIndices:
        #     P[index] = (XNorm[index] ** (-1/self.T) / sumDenom)
        #     P[XBestNIndices] = (XNorm[XBestNIndices] ** (-1 / self.T) / sumDenom)
        # TODO : No changes in the rest of the code are needed


        # Update the temperature
        self.T *= self._TEMPERATURE_DECAY_FACTOR

        return P

    # Find the next state to develop
    def _getNextState(self, problem, currState):
        successors = list(problem.expand(currState))
        P = self._getSuccessorsProbabilities(currState, successors)

        # TODO : Choose the next state stochastically according to the calculated distribution.
        # You should look for a suitable function in numpy.random.
        # choose a successor randomly with the probability from the instructions
        return np.random.choice(successors, 1, p=P)[0]

    # Override the base solve method to initialize the temperature
    def solve(self, initialState):
        self.T = self._INITIAL_TEMPERATURE
        return super().solve(initialState)