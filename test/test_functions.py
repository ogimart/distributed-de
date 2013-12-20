import math
import numpy
import de


class FunctionResult:
    """
    FunctionResult holds DE results and desired accuracy used in unittest.
    Arguments:
        minimum - function minimum
        min_point - point cooridinates where function has a minimum
        places - decimal places accuracy for minimum
        lower - sequence od lower bounds for min_point
        upper - sequence od upper bounds for min_point
            lower[i] < min_point[i] < upper[i] 
    """
    def __init__(self, minimum, min_point, places, lower, upper):
        self.minimum = minimum
        self.min_point = min_point
        self.places = places
        self.lower = lower
        self.upper = upper

eps = 1e-05

def func1(x):
    """
    Function 1 - Sphere (first De Jong function)
    Two parameters in range [-5.12, 5.12]
    The minimum is f(0,0) = 0
    """
    return x[0]**2 + x[1]**2

sphere = de.Function(func1, 2, (-5.12, -5.12), (5.12, 5.12))
sphere_result = FunctionResult(0., (0., 0.), 7, (-eps, -eps), (eps, eps))

def func2(x):
    """
    Function 2 - Rosenbrock's saddle (second De Jong function)
    Two parameters in range [-2.048, 2.048]
    The minimum is f(1,1) = 0
    """
    return 100*(x[0]**2 - x[1])**2 + (1 - x[0])**2

saddle = de.Function(func2, 2, (-2.048,)*2, (2.048,)*2)
saddle_result = FunctionResult(0., (1., 1.), 7, (1.-eps,)*2, (1.+eps,)*2)

def func3(x):
    """
    Function 3 - Step (third De Jong function)
    Four parameters in range [-5.12, 5.12]
    The minimum is f(-5-e,..,-5-e) = 0 where e is in range [0,0.12]
    """
    floor = numpy.floor(x)
    return 30 + floor.sum()

step = de.Function(func3, 5, (-5.12,)*5, (5.12,)*5)
step_result = FunctionResult(0., (-5,)*5, 7, (-5.12,)*5, (-5.,)*5)

def func4(x):
    """
    Function 4 - Griewangk's function
    Nine parameters in range [-400, 400]
    The minimum is f(0,..,0) = 0
    """
    s = 0.
    for j in range(9):
        s += x[j]**2/4000
    p = 1.
    for j in range(9):
        p *= math.cos(x[j]/math.sqrt(j+1))
    return s - p + 1

griewangk = de.Function(func4, 9, (-400,)*9, (400,)*9)
griewangk_result = FunctionResult(0., (0.,)*9, 7, (-eps,)*9, (eps,)*9)
