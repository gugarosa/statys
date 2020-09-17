class Analyzer:
    """
    """

    def __init__(self, *args):
        """
        """

        #
        for i, arg in enumerate(args):
            #
            attr = f'arg{i}'

            #
            setattr(self, attr, arg)

    def __repr__(self):
        """
        """

        return str(self.__dict__)

    @property
    def attrs(self):
        """
        """

        return self.__dict__.items()
