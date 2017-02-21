"""
from unittest import TestSuite

from qube.test.test_hello_controller import TestHelloController
from qube.test.test_hello_services import TestHelloService
from qube.test.test_hello_model import TestHelloModel

test_cases = (TestHelloController, TestHelloService, TestHelloModel)

def load_tests(loader, tests, pattern):
    suite = TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite
"""