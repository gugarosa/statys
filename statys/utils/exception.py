"""Exceptions.
"""

import statys.utils.logging as l

logger = l.get_logger(__name__)


class Error(Exception):
    """A generic Error class derived from Exception.

    Essentially, it gets the class and message and logs the error to the logger.

    """

    def __init__(self, cls, msg):
        """Initialization method.

        Args:
            cls (str): Class identifier.
            msg (str): Message to be logged.

        """

        # Override its parent class
        super(Error, self).__init__()

        # Logs the error in a formatted way
        logger.error('%s: %s.', cls, msg)


class ArgumentError(Error):
    """An ArgumentError class for logging errors related to wrong number of provided arguments.

    """

    def __init__(self, error):
        """Initialization method.

        Args:
            error (str): Error message to be logged.

        """

        # Override its parent class with class name and error message
        super(ArgumentError, self).__init__('ArgumentError', error)


class SizeError(Error):
    """A SizeError class for logging errors related to wrong length or size of variables.

    """

    def __init__(self, error):
        """Initialization method.

        Args:
            error (str): Error message to be logged.

        """

        # Override its parent class with class name and error message
        super(SizeError, self).__init__('SizeError', error)


class TypeError(Error):
    """A TypeError class for logging errors related to wrong type of variables.

    """

    def __init__(self, error):
        """Initialization method.

        Args:
            error (str): Error message to be logged.

        """

        # Override its parent class with class name and error message
        super(TypeError, self).__init__('TypeError', error)


class ValueError(Error):
    """A ValueError class for logging errors related to wrong value of variables.

    """

    def __init__(self, error):
        """Initialization method.

        Args:
            error (str): Error message to be logged.

        """

        # Override its parent class with class name and error message
        super(ValueError, self).__init__('ValueError', error)
