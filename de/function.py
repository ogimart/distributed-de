import numpy as np


class Function(object):
    """
    Function wrapper used in Differential Evolution algorithms

    Public members initialized in constructor: 
    func  -- function to be minimized func(x)
             where x is a numerical sequence of function parameters
    dim   -- number of function parameters (length of x)
    lower -- lower bounds for function parameters
             numerical sequence of length dim
    upper -- upper bounds for function parameters
             numerical sequence of length dim

    Function func(x) must be continuous for all:
            lower[i] <= x[i] < upper[i] where i in [0, dim)

    Example:
    >>> def func(x):
    ...     return x[0]**2 + x[1]**2
    ...
    >>> sphere = Function(func, 2, (-10,-10), (10,10))
    """

    def __init__(self, func, dim, lower, upper):
        """
        Initializes public member func, dim, lower and upper

        Arguments:
        func  -- function to be minimized func(x)
                 where x is a numerical sequence of function parameters
        dim   -- number of function parameters (length of x)
        lower -- lower bounds for function parameters
                 numerical sequence of length dim
        upper -- upper bounds for function parameters
                 numerical sequence of length dim

        Note:
            Function func(x) must be continuous for all:
                lower[i] <= x[i] < upper[i] where i in [0, dim)
    
        Exceptions:
            TypeError, ValueError
        """

        if not hasattr(func, '__call__'):
            raise TypeError('func is not a callable')

        if not int(dim) > 0:
            raise ValueError('dim must be positive integer')

        if dim != len(lower):
            raise ValueError('length of lower must be equal to dim')

        if dim != len(upper):
            raise ValueError('length of upper must be equal to dim')

        if not (np.array(upper) > np.array(lower)).all():
            raise ValueError('lower must be less than upper for all elements')

        self.func = func
        self.dim = dim
        self.lower = lower
        self.upper = upper

    def __call__(self, x):
        """ 
        Returns func(x)

        Arguments:
        x -- must be numerical sequence of length dim 

        Exceptions:
            ValueError
        """
        if len(x) != self.dim:
            raise ValueError('number of func parameters different than dim')

        return self.func(x)


# doctest
if __name__ == "__main__":
    import doctest
    doctest.testmod()
