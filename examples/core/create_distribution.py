from statys.core import Distribution

# Defining input arguments
x = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
y = [0.07, 0.14, 0.72, 0.32, 0.59]

# Creating the distribution
d = Distribution(x, y)

# Printing out its attributes
print(d)
