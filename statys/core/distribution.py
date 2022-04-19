"""Distribution-related definitions.
"""

from typing import Any, Dict

import numpy as np

import statys.utils.exception as e
from statys.utils import logging

logger = logging.get_logger(__name__)


class Distribution:
    """A class that serves as the foundation for calculating statistical analysis. In other words,
    one can interpret this class as the population.

    """

    def __init__(self, *args) -> None:
        """Initialization method."""

        logger.info("Initializing class with %d arguments ...", len(args))

        for i, arg in enumerate(args):
            attr = f"arg{i}"

            if not isinstance(arg, (list, np.ndarray)):
                raise e.TypeError(f"`{attr}` should be a list or np.ndarray")

            setattr(self, attr, arg)

        logger.debug("%s", self)
        logger.info("Class initialized.")

    def __repr__(self) -> str:
        """Class' string representation.

        Returns:
            (str): String representation.

        """

        return str(self.__dict__)

    @property
    def attrs(self) -> Dict[str, Any]:
        """Gathers all attributes from class.

        Returns:
            (Dict[str, Any]): Attributes encoded into a dictionary.

        """

        return self.__dict__.items()
