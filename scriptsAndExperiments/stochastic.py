from sympy.strategies.tree import greedy

from consts import Consts
from astar import AStar
from ways import load_map_from_csv
from busSolvers import GreedyBestFirstSolver, GreedyStochasticSolver
from problems import BusProblem
from costs import L2DistanceCost
from heuristics import L2DistanceHeuristic
import numpy as np

REPEATS = 150

# Load the files
roads = load_map_from_csv(Consts.getDataFilePath("israel.csv"))
prob = BusProblem.load(Consts.getDataFilePath("HAIFA_100.in"))

mapAstar = AStar(L2DistanceHeuristic(), shouldCache=True)

scorer = L2DistanceCost(roads)

# Run the greedy solver
pickingPath = GreedyBestFirstSolver(roads, mapAstar, scorer).solve(prob)
greedyDistance = pickingPath.getDistance() / 1000
print("Greedy solution: {:.2f}km".format(greedyDistance))

# Run the stochastic solver #REPATS times
solver = GreedyStochasticSolver(roads, mapAstar, scorer,
                                Consts.STOCH_INITIAL_TEMPERATURE,
                                Consts.STOCH_TEMPERATURE_DECAY_FUNCTION,
                                Consts.STOCH_TOP_SCORES_TO_CONSIDER)
results = np.zeros((REPEATS,))
print("Stochastic repeats:")
for i in range(REPEATS):
    print("{}..".format(i+1), end=" ", flush=True)
    results[i] = solver.solve(prob).getDistance() / 1000

print("\nDone!")

# TODO : Part1 - Plot the diagram required in the instructions
from matplotlib import pyplot as plt

# keeping the resualts monotonic
monotonicResults = [0] * len(results)
monotonicResults[0] = results[0]

for i in range(1,len(results)):
    if results[i] < monotonicResults[i-1]:
        monotonicResults[i] = results[i]
    else:
        monotonicResults[i] = monotonicResults[i - 1]
# construct both greedy and stochastic graphs
plt.plot(range(1, REPEATS+1), [greedyDistance] * REPEATS, label="deterministic greedy")
plt.plot(range(1, REPEATS+1), monotonicResults, label="stochastic greedy")
plt.title("Comparison of deterministic greedy vs. stochastic greedy")
plt.xlabel("# Iteration")
plt.legend(bbox_to_anchor=(1, 1))
plt.show()


# TODO : Part2 - Remove the exit and perform the t-test
from scipy import stats as spstats

stochasticMean = np.mean(results)
stochasticStd = np.std(results)

print("statistic results of greedy stochastic: Mean: {} Standard Deviation: {}".format(stochasticMean,stochasticStd))

_, pValue = spstats.ttest_1samp(results, greedyDistance)

print("pValue of Ttest: {}".format(pValue))