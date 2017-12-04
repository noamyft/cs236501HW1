import numpy as np
import sys

class AStar:
    cost = None
    heuristic = None
    _cache = None
    shouldCache = None

    def __init__(self, heuristic, cost=None, shouldCache=False):
        self.heuristic = heuristic
        self.shouldCache = shouldCache
        self.cost = cost

        # Handles the cache. No reason to change this code.
        if self.shouldCache:
            self._cache = {}

    # Get's from the cache. No reason to change this code.
    def _getFromCache(self, problem):
        if self.shouldCache:
            return self._cache.get(problem)

        return None

    # Get's from the cache. No reason to change this code.
    def _storeInCache(self, problem, value):
        if not self.shouldCache:
            return

        self._cache[problem] = value

    # Run A*
    def run(self, problem):
        # Check if we already have this problem in the cache.
        # No reason to change this code.
        source = problem.initialState
        if self.shouldCache:
            res = self._getFromCache(problem)

            if res is not None:
                return res

        # Initializes the required sets
        closed_set = set()  # The set of nodes already evaluated.
        parents = {}  # The map of navigated nodes.

        # Save the g_score and f_score for the open nodes
        g_score = {source: 0}
        open_set = {source: self.heuristic.estimate(problem, problem.initialState)}

        developed = 0

        # TODO : Implement astar.
        # Tips:
        # - To get the successor states of a state with their costs, use: problem.expandWithCosts(state, self.cost)
        # - You should break your code into methods (two such stubs are written below)
        # - Don't forget to cache your result between returning it - TODO
        while open_set:
            next = self._getOpenStateWithLowest_f_score(open_set)
            closed_set.add(next)
            del open_set[next]
            developed += 1 # count next as a developed node
            #  check if we reached the goal
            if problem.isGoal(next):
                res = (self._reconstructPath(parents,next), g_score[next],
                        self.heuristic.estimate(problem, problem.initialState), developed)
                self._storeInCache(problem,res)
                return res
            # loop over sons of next
            for (s,costEdge) in problem.expandWithCosts(next,self.cost):
                new_g = g_score[next] + costEdge
                newScore = new_g + self.heuristic.estimate(problem, s)
                # we all ready created the node
                if s in open_set:
                    # new g is better that the one we have
                    if g_score[s] > new_g:
                        open_set[s] = newScore
                        g_score[s] = new_g
                        parents[s] = next
                # we all ready developed this node
                elif s in closed_set:
                    # new g is better that the one we have
                    if g_score[s] > new_g:
                        g_score[s] = new_g
                        parents[s] = next
                        closed_set.discard(s)
                        open_set[s] = newScore
                # first time we encounter this node
                else:
                    g_score[s] = new_g
                    parents[s] = next
                    open_set[s] = newScore
        raise Exception("No path to goal!!!")

    def _getOpenStateWithLowest_f_score(self, open_set):
        min = None
        for (key,value) in open_set.items():
            if min is None:
                min = (key,value)
            else:
                min = (key,value) if value < min[1] else min
        return min[0]



    # Reconstruct the path from a given goal by its parent and so on
    def _reconstructPath(self, parents, goal):
        res = [goal]
        current = goal
        while current in parents:
            res.insert(0,parents[current])
            current = parents[current]
        return res
