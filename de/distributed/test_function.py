from de import Function

def func(x):
    return 100*(x[0]**2 - x[1])**2 + (1 - x[0])**2
     
saddle = Function(func, dim=2, lower=(-2.048,)*2, upper=(2.048,)*2)
