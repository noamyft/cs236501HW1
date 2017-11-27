from . import Heuristic
from ways import tools, compute_distance
import problems

# Use the L2 aerial distance (in meters)
class L2DistanceHeuristic(Heuristic):
    def estimate(self, problem, state):
        coord1 = problem._roads[state.junctionIdx].coordinates
        coord2 = problem.target.coordinates
        return compute_distance(coord1, coord2)

