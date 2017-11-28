from functools import reduce

from . import GreedySolver
import numpy as np

class GreedyBestFirstSolver(GreedySolver):
    def __init__(self, roads, astar, scorer):
        super().__init__(roads, astar, scorer)

    # Find the next state to develop
    def _getNextState(self, problem, currState):
        successors = list(problem.expand(currState))
        #if successors:
        closest_state = reduce(lambda x,y: x if self._scorer.compute(currState, x) < self._scorer.compute(currState, y)
                                else y, successors)
        return closest_state