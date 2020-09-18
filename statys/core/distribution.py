"""Distribution-related definitions.
"""

import numpy as np

import statys.utils.exception as e
import statys.utils.logging as l

logger = l.get_logger(__name__)


class Distribution:
    """A class that serves as the foundation for calculating statistical analysis. In other words,
    one can interpret this class as the population.

    """

    def __init__(self, *args):
        """Initialization method.

        """

        logger.info('Initializing class with %d arguments ...', len(args))

        # Iterates through every argument
        for i, arg in enumerate(args):
            # Defines the argument's name
            attr = f'arg{i}'

            # Checks the argument type
            if not isinstance(arg, (list, np.ndarray)):
                # Raises an error
                raise e.TypeError(f'`{attr}` should be a list or np.ndarray')

            # Sets the argument
            setattr(self, attr, arg)

        logger.debug('%s', self)
        logger.info('Class initialized.')

    def __repr__(self):
        """Class' string representation.

        """

        return str(self.__dict__)

    @property
    def attrs(self):
        """Gathers all attributes from class.

        """

        return self.__dict__.items()
