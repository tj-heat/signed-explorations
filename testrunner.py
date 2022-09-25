import unittest

# Test modules
import tests.util.test_ring_buffer as test_ring_buffer

# initialize the test suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# Add tests to suite
suite.addTests(loader.loadTestsFromModule(test_ring_buffer))

# Initialise runner and run tests
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)