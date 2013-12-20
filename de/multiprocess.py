import ctypes
import multiprocessing as mp
import numpy as np
import numpy.random as rnd

from function import Function
from diffevol import _DifferentialEvolution
from singleprocess import DifferentialEvolutionSP


class DifferentialEvolutionMP(_DifferentialEvolution):
    """ 
    Differential Evolution algorithm - multi process implementation.

    Public members initialized in constructor:
    pop_size   -- population size, integer constant greater than zero
                  (recomended at least 10x number of function parameters)
    max_gen    -- maximum generations, integer constant greater than zero
                  (recomended at least 1000)
    cr         -- crossover constant, float in [0,1]
    f          -- factor of differential amplification, float in [0,2]
    proc_count -- number of processes, integer greater or equal to zero
                  if zero then multiprocessing.cpu_count() is used

    Example:
    >>> def func(x):
    ...     return 100*(x[0]**2 - x[1])**2 + (1 - x[0])**2
    >>> 
    >>> saddle = Function(func, dim=2, lower=(-2.048,)*2, upper=(2.048,)*2)
    >>> de = DifferentialEvolutionMP(pop_size=40, max_gen=1000, cr=0.9, f=0.9,
    ...                              proc_count=2)
    >>> minimum, min_point = de.find_min(saddle)
    >>> 
    >>> print "Min: f", tuple(min_point), "=", minimum
    Min: f (1.0, 1.0) = 0.0
    """

    def __init__(self, pop_size=20, max_gen=1000, cr=0.9, f=0.5, 
                 proc_count=1):

        super(DifferentialEvolutionMP, self).__init__(pop_size, max_gen, cr, f)

        if not proc_count >= 0:
            raise ValueError('proc_count must be integer >= 0')

        if proc_count == 0:
            self.proc_count = mp.cpu_count()
        else:
            self.proc_count = proc_count

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

        # shared mememory among processes
        self._shmem_cost = mp.RawArray(ctypes.c_double, self.pop_size)
        self._shmem_x = mp.RawArray(ctypes.c_double, self.pop_size*func.dim)

        # create processes and population slices
        slice_len = int(self.pop_size/self.proc_count)
        proc_group = []
        for i in range(self.proc_count - 1):
            slice_start = i*slice_len
            slice_end = i*slice_len + slice_len
            p = mp.Process(target=self._run_de, 
                           args=(func, slice_start, slice_end))
            proc_group.append(p)
        # handle uneven last slice
        p = mp.Process(target=self._run_de, 
                       args=(func, (self.proc_count-1)*slice_len, 
                             self.pop_size))
        proc_group.append(p)

        # start all then join all
        for proc in proc_group:
            proc.start()
        for proc in proc_group:
            proc.join()

        # copy results from shared memory
        self._cost = np.frombuffer(self._shmem_cost) 
        self._x = np.reshape(np.frombuffer(self._shmem_x), 
                             (self.pop_size, func.dim))
 
        # find min
        min_index = self._cost.argmin()
        return self._cost[min_index], self._x[min_index]
 
    def _run_de(self, func, slice_start, slice_end):
        """
        Implementation of DE algorithm.
        It's run in a process that creates and runs DifferentialEvolutionSP.
        Populates _shmem_cost and population _shmem_x shared raw arrays.
        """ 
         # run single process de on a population slice
        slice_size = slice_end - slice_start
        sp = DifferentialEvolutionSP(slice_size, self.max_gen, 
                                     self.cr, self.f)
        sp.find_min(func)

        # copy results to shared memory
        self._shmem_cost[slice_start : slice_end] = sp._cost[:]
        self._shmem_x[slice_start*func.dim : slice_end*func.dim] = \
            sp._x.flatten()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
