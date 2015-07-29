# Distributed Differential Evolution

## About

Python implementation of Differential Evolution algorgitm. It's a fast converging algorhithm for finding global optima of hard to optimize multidimensional real valued functions. It can utilize multi-processor and multi-core machines or it can be distributed over the network.

## Dependencies

* Python 2.7
* NumPy

## Basic Usage

	In [1]: import de
	In [2]: def func(x):
    			return 100*(x[0]**2 - x[1])**2 + (1 - x[0])**2
	In [3]: saddle = de.Function(func, 2, (-2.048,)*2, (2.048,)*2)
	In [4]: diffevol = de.DifferentialEvolutionMP(pop_size=40, f=0.9, cr=0.9, proc_count=4)
	In [5]: min, pt = diffevol.find_min(saddle)
	In [6]: min, pt
	Out[6]: (0.0, array([ 1.,  1.]))
	
Example above (using iPyhon), first imports de module, then creates a function to be optimized. In this case it's Rosenbrock's saddle. The third step creates DE function object 'saddle' passing to constructor: function to be optimized, number of function parameters, and lower and upper bounds of the function. Fourth step instanciets differenctial algorithm. Parameters passed to constructor are algorithm population size, factor of differential amplification f, cross over rate cr, and the number of processors. Fifth steps runs the algorhitm. The result is tuple where the first element is the minimum of the function, and the second element is array with parameters where functions has a minimum.

## Tests

To run unit tests:

	$ cd distributed_de/test
	$ python unittest_suite.py 

More detailed documentation can be found in the doc strings. More examples can be found in the test code.


	



