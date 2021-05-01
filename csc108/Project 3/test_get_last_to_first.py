"""A3. Test cases for function club_functions.get_last_to_first.
"""

import unittest
import club_functions


class TestGetLastToFirst(unittest.TestCase):
    """Test cases for function club_functions.get_last_to_first.
    """

    def test_00_empty(self):
        param = {}
        actual = club_functions.get_last_to_first(param)
        expected = {}
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_01_one_person_one_friend_same_last(self):
        param = {'Clare Dunphy': ['Phil Dunphy']}
        actual = club_functions.get_last_to_first(param)
        expected = {'Dunphy': ['Clare', 'Phil']}
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)
        
    def test_02_one_person_same_first_last(self):
        param = {'Clare Dunphy': ['Clare Dunphy']}
        actual = club_functions.get_last_to_first(param)
        expected = {'Dunphy': ['Clare']}
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)    
        
    def test_03_one_person_and_friend_multiple_first(self):
        param = {'Clare-Test Dunphy': ['John A Doe']}
        actual = club_functions.get_last_to_first(param)
        expected = {'Dunphy': ['Clare-Test'], 'Doe': ['John A']}
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)
    
    def test_04_one_person_multiple_friends(self):
        param = {'Clare-Test Dunphy': ['John A Doe', 'John Smith', \
                                       'Alex Smith', 'John Dan']}
        actual = club_functions.get_last_to_first(param)
        expected = {'Dunphy': ['Clare-Test'], 'Doe': ['John A'], \
                    'Smith': ['Alex', 'John'], 'Dan': ['John']}
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)       
        
    def test_05_two_persons_same_friend(self):
        param = {'Clare-Test Dunphy': ['John A Doe'], \
                 'Testing Test': ['John A Doe']}
        actual = club_functions.get_last_to_first(param)
        expected = {'Dunphy': ['Clare-Test'], 'Doe': ['John A'], \
                    'Test': ['Testing']}
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)         
    
    def test_06_two_persons_multiple_friends(self):
        param = {'Clare-Test Dunphy': ['John A Doe', 'John Smith', \
                                       'Alex Smith', 'John Dan-E'], \
                 'Testing Test': ['John A Doe', 'Clare-Test Dunphy', \
                                  'Jane Doe', 'A Doe']}
        actual = club_functions.get_last_to_first(param)
        expected = {'Dunphy': ['Clare-Test'], 'Doe': ['A', 'Jane', 'John A'], \
                    'Dan-E': ['John'], 'Smith': ['Alex', 'John'], \
                    'Test': ['Testing']}
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)       

if __name__ == '__main__':
    unittest.main(exit=False)
