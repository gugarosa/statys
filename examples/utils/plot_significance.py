import statys.tests.wilcoxon as w
import statys.utils.plotter as p
from statys.core import Distribution

# Defining input arguments
x = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
y = [0.07, 0.14, 0.72, 0.32, 0.59, 0.43]
z = [2.17, 9.14, 999.72, 8.32, 7.19, 9.43]

# Creating the distribution
d = Distribution(x, y, z)

# Calculating Wilcoxon's signed-rank test
signed_rank = w.signed_rank(d)

# Plots the significance indexes
p.plot_significance_index(signed_rank, title='Wilcoxon Signed-Rank Test ($h$-index)')
