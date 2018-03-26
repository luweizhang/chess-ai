"""tests go here"""
import unittest

def add(a, b):
    """This function adds two numbers a, b and returns their sum
    a and b may integers
    """
 
    if isinstance(a, int) and isinstance(b, int):
        return a + b
    elseif isinstance(a, str) and isinstance(b, str):
        return int(a) + intg(b)
    else:
        raise Exception('Invalid arguments')
 
class Test(unittest.TestCase):
    def test_add(self):
        self.assertEqual(5, add(2, 3))
        self.assertEqual(15, add(-6, 21))
        self.assertRaises(Exception, add, 4.0, 5.0)
