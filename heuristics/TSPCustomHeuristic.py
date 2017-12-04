from heuristics import Heuristic
from ways import tools, compute_distance


# TODO : Implement as explained in the instructions
class TSPCustomHeuristic(Heuristic):
    _distMat = None
    _junctionToMatIdx = None

    # TODO : You can add parameters if you need them
    def __init__(self, roads, initialState):
        self.roads = roads
        self.initialState = initialState

    # Estimate heuristically the minimal cost from the given state to the problem's goal
    # Using d heuristic from instructions
    # returns the maximum distance between current state and si from Waiting List
    def estimate(self, problem, state):
        maxDistance = 0
        coord = self.roads[state.junctionIdx].coordinates # coordination of current state
        for order1 in state.waitingOrders:
            coord1 = self.roads[order1[0]].coordinates  # coordination of si from Waiting List
            curr = compute_distance(coord1, coord)     # distance between current state and si
            maxDistance = max(curr,maxDistance)
        return maxDistance