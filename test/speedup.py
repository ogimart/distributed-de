import timeit

setup = """\
import test_functions as fn
import de

pop_size = 160 
max_gen = 1000
cr = 0.9
f = 0.5
cpu = 8

sp = de.DifferentialEvolution(pop_size, max_gen, cr, f)
mp = de.DifferentialEvolutionMP(pop_size, max_gen, cr, f, cpu)
"""
t_sp = timeit.Timer("sp.find_min(fn.saddle)", setup)
t_mp = timeit.Timer("mp.find_min(fn.saddle)", setup)
t1 = t_sp.timeit(10)
t2 = t_mp.timeit(10)
print "Single process: ", t1
print "Multi-process: ", t2
print "Speed up: ", t1/t2

