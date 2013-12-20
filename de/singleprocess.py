import numpy as np
import numpy.random as rnd

from function import Function
from diffevol import _DifferentialEvolution


class DifferentialEvolutionSP(_DifferentialEvolution):
    """ 
    Differential Evolution algorithm - single process implementation.

    Public members initialized in constructor:
    pop_size -- population size, integer constant greater than zero
                (recomended at least 10x number of function parameters)
    max_gen  -- maximum generations, integer constant greater than zero
                (recomended at least 1000)
    cr       -- crossover constant, float in [0,1]
    f        -- factor of differential amplification, float in [0,2]

    Example:
    >>> def func(x):
    ...     return 100*(x[0]**2 - x[1])**2 + (1 - x[0])**2
    >>> 
    >>> saddle = Function(func, dim=2, lower=(-2.048,)*2, upper=(2.048,)*2)
    >>> de = DifferentialEvolutionSP(pop_size=40, max_gen=1000, cr=0.9, f=0.9)
    >>> minimum, min_point = de.find_min(saddle)
    >>> 
    >>> print "Min: f", tuple(min_point), "=", minimum
    Min: f (1.0, 1.0) = 0.0
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

        super(DifferentialEvolutionSP, self).__init__(pop_size, max_gen, cr, f)

    def find_min(self, func):
        """
        Returns tuple consisting of:
        - function minimum
        - point where function has a minimum (numpy array)

        Arguments:
        func -- function to be minimized, instance of Function
        
        Exceptions:
            TypeError
        """
        self._check_func(func)

        self._run_de(func)
        min_index = self._cost.argmin()
        return self._cost[min_index], self._x[min_index]
 
    def _run_de(self, func):
        """
        Implementation of DE algorithm
        Populates _cost (1d numpy) and population _x (2d numpy) 
        """ 
        dim = func.dim
        lower = np.array(func.lower)
        upper = np.array(func.upper)

        self._x = rnd.rand(self.pop_size, dim)*(upper - lower) + lower
        self._cost = np.zeros(self.pop_size)
        trial = np.zeros(dim)

        for i in range(self.pop_size):
            self._cost[i] = func(self._x[i])

        for g in range(self.max_gen):
            for i in range(self.pop_size): 
                a, b, c = self._unique_indexes(i, self.pop_size);
                j = rnd.randint(0, dim)

                for k in range(1, dim + 1):
                    if rnd.rand() < self.cr or k == dim:
                        trial[j] = (self._x[c,j] + 
                                    self.f*(self._x[a,j] - self._x[b,j]))
                        if trial[j] < lower[j] or trial[j] > upper[j]:
                            trial[j] = (rnd.rand(1)[0]*(upper[j] - lower[j]) +
                                lower[j])
                    else:
                        trial[j] = self._x[i,j]
                    j = (j+1) % dim

                score = func(trial)
                if score <= self._cost[i]:
                    self._x[i] = np.copy(trial)
                    self._cost[i] = score

    def _unique_indexes(self, idx, bound):
        """
        Returns three unique random integers a, b, c in range [0,bound) where:
        a != idx, b != idx, and c != idx
        """
        a = b = c = idx
        while a == idx:
            a = rnd.randint(0, bound)
        while b == idx or a == b:
            b = rnd.randint(0, bound)
        while c == idx or c == a or c == b:
            c = rnd.randint(0, bound)
        return a, b, c


if __name__ == "__main__":
    import doctest
    doctest.testmod()
