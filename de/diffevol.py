from function import Function

class _DifferentialEvolution(object):
    """ 
    Differential Evolution private base class, holds algorithm parameters.

    Public members initialized in constructor:
    pop_size -- population size, integer constant greater than zero
                (recomended at least 10x number of function parameters)
    max_gen  -- maximum generations, integer constant greater than zero
                (recomended at least 1000)
    cr       -- crossover constant, float in [0,1]
    f        -- factor of differential amplification, float in [0,2]

    Example:
    >>> def func(x):
    ...     return x[0]**2 + x[1]**2
    >>> 
    >>> sphere = Function(func, dim=2, lower=(-2.048,)*2, upper=(2.048,)*2)
    >>> de = _DifferentialEvolution(pop_size=40, max_gen=1000, cr=0.9, f=0.9)
    >>> de._check_func(sphere)
    >>> 
    """

    def __init__(self, pop_size=20, max_gen=1000, cr=0.9, f=0.5):
        """
        Initializes public members pop_size, max_gen, cr and f.

        Arguments:
        pop_size -- population size, integer constant greater than zero
                    (recomended at least 10x number of function parameters)
        max_gen  -- maximum generations, integer constant greater than zero
                    (recomended at least 1000)
        cr       -- crossover constant, float in [0,1]
        f        -- factor of differential amplification, float in [0,2]

        Exceptions:
            ValueError
        """

        if not pop_size > 0:
            raise ValueError('pop_size must be integer greater than zero')

        if not max_gen > 0:
            raise ValueError('max_gen must be integer greater than zero')

        if not (cr >= 0 and cr <= 1):
            raise ValueError('cr must be float in range [0,1]')

        if not (f >= 0 and cr <= 2):
            raise ValueError('f must be float in range [0,2]')

        self.pop_size = pop_size
        self.max_gen = max_gen
        self.cr = cr
        self.f = f

    def _check_func(self, func):
        """
        Checks if func is instance of Function.

        Arguments:
        func -- function to be minimized, instance of Function
        
        Exceptions:
            TypeError
        """
        if not isinstance(func, Function):
            raise TypeError('func must be instance of Function')

if __name__ == "__main__":
    import doctest
    doctest.testmod()
