import numpy as np
from matplotlib import pyplot as plt

X = np.array([400,900,390,1000,550])

# TODO : Write the code as explained in the instructions
XNorm = X / np.min(X)

T = np.linspace(0.01, 5.0,100)
exponent = -1/T

i = 0
for num in XNorm:
    probability = [num**t/np.sum(XNorm**t) for t in exponent]

    plt.plot(T, probability, label=str(X[i]))
    i += 1

plt.title("Probability as a function of the temperature")
plt.xlabel("T")
plt.legend(bbox_to_anchor=(1, 1), borderaxespad=0.)
plt.show()