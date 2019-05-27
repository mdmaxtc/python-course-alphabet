import unittest
import calc


class CalcTest(unittest.TestCase):
    # """Calc tests"""
    #
    # @classmethod
    # def setUpClass(cls):
    #     """Set up for class"""
    #     print('setUpClass')
    #     print('==========')
    #
    # @classmethod
    # def tearDownClass(cls):
    #     """Tear down for class"""
    #     print('tearDownClass')
    #     print('==========')
    #
    # def setUp(self):
    #     """Set up for test"""
    #     print(f"Set up for [{self.shortDescription()}]")
    #
    # def TearDown(self):
    #     """Tear down for test"""
    #     print(f"Tear down for [{self.shortDescription()}]")

    def test_add(self):
        self.assertEqual(calc.add(1, 2), 3)

    def test_sub(self):
        self.assertEqual(calc.sub(4, 2), 2)

    def test_mult(self):
        self.assertEqual(calc.mult(5, 2), 10)

    def test_div(self):
        self.assertEqual(calc.div(8, 4), 2)


if __name__ == '__main__':
    unittest.main()