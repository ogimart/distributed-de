import unittest

import de
import test_functions as fn


class TestDifferentialEvolutionSP(unittest.TestCase):

    def assertResult(self, minimum, point, func_res):
        """
        Check if minimum has accuracy to the desired decimal places 
        Check if mimimum point is within the accuracy bounds
        """
        self.assertAlmostEqual(minimum, func_res.minimum, func_res.places)
        for i in range(len(point)):
            self.assertGreater(point[i], func_res.lower[i])
            self.assertLess(point[i], func_res.upper[i])

    def testSphere(self):
        self.assertIsInstance(fn.sphere, de.Function)
        self.assertIsInstance(fn.sphere_result, fn.FunctionResult)
        diffevol = de.DifferentialEvolutionSP(pop_size=20, f=0.9, cr=0.1)
        minimum, point = diffevol.find_min(fn.sphere)
        self.assertResult(minimum, point, fn.sphere_result)

    def testSaddle(self):
        self.assertIsInstance(fn.saddle, de.Function)
        self.assertIsInstance(fn.saddle_result, fn.FunctionResult)
        diffevol = de.DifferentialEvolutionSP(pop_size=40, f=0.9, cr=0.9)
        minimum, point = diffevol.find_min(fn.saddle)
        self.assertResult(minimum, point, fn.saddle_result)

    def testStep(self):
        self.assertIsInstance(fn.step, de.Function)
        self.assertIsInstance(fn.step_result, fn.FunctionResult)
        diffevol = de.DifferentialEvolutionSP(pop_size=50, f=0.9, cr=0)
        minimum, point = diffevol.find_min(fn.step)
        self.assertResult(minimum, point, fn.step_result)

    def testGriewangk(self):
        self.assertIsInstance(fn.griewangk, de.Function)
        self.assertIsInstance(fn.griewangk_result, fn.FunctionResult)
        diffevol = de.DifferentialEvolutionSP(pop_size=90, f=0.5, cr=0.2)
        minimum, point = diffevol.find_min(fn.griewangk)
        self.assertResult(minimum, point, fn.griewangk_result)


def suite():
   suite = unittest.TestSuite()
   suite.addTest(unittest.makeSuite(TestDifferentialEvolutionSP))
   return suite

if __name__ == '__main__':
    unittest.main()

"""
def run_de(mod_name, func_name, dim, lower, upper,
           pop=20, max_gen=1000, cr=0.9, f=0.5):
    m = __import__(mod_name)
    func = getattr(m, func_name)
    return de.find_min(func, dim, lower, upper, pop, max_gen, cr, f)
"""
