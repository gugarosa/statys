from statys.core import Distribution
import statys.tests.measure as m
import statys.tests.wilcoxon as w
import numpy as np

x = np.arange(20) + np.arange(1,21)/100.0
y = np.array(np.arange(1, 21))
y = y - 1
y[15:] += 1

print(x, y)

a = Distribution(x, y)

print(m.mean(a), m.std(a))

# print(w.wilcoxon_signed_rank(a))
# print(w.wilcoxon_rank_sum(a))