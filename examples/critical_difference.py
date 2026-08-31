import numpy as np

from statys import nemenyi, plot_critical_difference

scores = np.array(
    [
        [0.82, 0.79, 0.75],
        [0.80, 0.77, 0.78],
        [0.84, 0.81, 0.76],
        [0.79, 0.75, 0.74],
    ]
)
ranks, critical_difference = nemenyi(scores)
plot_critical_difference(
    ranks,
    critical_difference,
    labels=["Model A", "Model B", "Model C"],
    output="critical-difference.pdf",
)
