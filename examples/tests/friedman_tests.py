import statys.tests.friedman as f
from statys.core import Distribution

# Defining input arguments
x = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
y = [0.07, 0.14, 0.72, 0.32, 0.59, 0.43]

# Creating the distribution
d = Distribution(x, y)

# Calculating Friedman-based tests
f.friedman(d)
f.friedman_with_posthoc(d)
