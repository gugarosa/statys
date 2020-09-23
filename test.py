import numpy as np

import statys.tests.measure as m
import statys.tests.non_parametric as n
from statys.core import Distribution

x = np.arange(20) + np.arange(1,21)/100.0
y = np.array(np.arange(1, 21))
y = y - 1
y[15:] += 1
z = y + 3.04

print(x, y)

a = Distribution(x, y, z)

# print(m.mean(a), m.std(a))

print(n.wilcoxon_signed_rank(a))
print(n.wilcoxon_rank_sum(a))
