import unittest
import unittest_sp
import unittest_mp

suite_sp = unittest_sp.suite()
suite_mp = unittest_mp.suite()

suite = unittest.TestSuite()
suite.addTest(suite_sp)
suite.addTest(suite_mp)
unittest.TextTestRunner(verbosity=3).run(suite)
