import statys.utils.plotter as p
import statys.tests.wilcoxon as w
from statys.core import Distribution

# Defining input arguments
x = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
y = [0.07, 0.14, 0.72, 0.32, 0.59, 0.43]
z = [0.17, 0.14, 0.72, 0.32, 0.19, 0.43]
l = [0.1, 0.14, 0.72, 0.32, 0.19, 0.03]

# Creating the distribution
d = Distribution(x, y, z)

wilc = w.signed_rank(d)

p.plot_similarity(wilc, labels=['a', 'b', 'c'])
