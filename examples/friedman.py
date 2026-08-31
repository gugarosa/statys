import numpy as np

from statys import friedman, nemenyi

scores = np.array(
    [
        [0.82, 0.79, 0.75],
        [0.80, 0.77, 0.78],
        [0.84, 0.81, 0.76],
        [0.79, 0.75, 0.74],
    ]
)

print(friedman(scores))
print(nemenyi(scores))
