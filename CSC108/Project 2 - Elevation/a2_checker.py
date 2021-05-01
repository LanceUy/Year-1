"""A simple checker for style errors and types of functions in
elevation.py.

"""

import unittest
import checker_generic
import elevation


class CheckTest(unittest.TestCase):
    """Sanity checker for assignment functions."""

    def test00CompareElevationsWithinRow(self):
        """Function compare_elevations_within_row."""

        self._returns_list_of_n_ints(elevation.compare_elevations_within_row,
                                     [[[1, 2], [2, 1]], 1, 1],
                                     3)

    def test01UpdateElevation(self):
        """Function update_elevation."""

        self._check_simple_type(
            elevation.update_elevation,
            [[[1, 2], [2, 1]], [0, 0], [0, 1], 2],
            type(None))

    def test02GetAverageElevation(self):
        """Function get_average_elevation"""

        self._check_simple_type(elevation.get_average_elevation,
                                [[[1, 2], [2, 1]]],
                                float)

    def test03FindPeak(self):
        """ Function find_peak"""

        self._returns_list_of_n_ints(elevation.find_peak,
                                     [[[1, 2], [2, 1]]],
                                     2)

    def test04IsSink(self):
        """Function is_sink"""

        self._check_simple_type(elevation.is_sink,
                                [[[1, 2], [2, 1]], [0, 0]],
                                bool)

    def test05FindLocalSink(self):
        """ Function find_local_sink"""
        self._returns_list_of_n_ints(elevation.find_local_sink,
                                     [[[1, 2], [2, 1]], [0, 0]],
                                     2)

    def test06CanHikeTo(self):
        """Function can_hike_to"""
        self._check_simple_type(
            elevation.can_hike_to,
            [[[1, 2], [2, 1]], [1, 1], [0, 0], 1],
            bool)

    def test07GetLowerResolution(self):
        """Function get_lower_resolution"""

        result = checker_generic.returns_list_of_Ts(
            elevation.get_lower_resolution,
            [[[1, 3, 4, 2], [2, 1, 1, 2], [4, 1, 1, 4], [3, 2, 1, 4]]],
            list)
        self.assertTrue(result[0], result[1])
        self.assertTrue(result[1] != [],
                        'get_lower_resolution should return a non-empty list')
        msg = checker_generic.type_error_message('get_lower_resolution',
                                                 'List[List[int]]',
                                                 result[1])
        for sublist in result[1]:
            self.assertTrue(
                sublist != [],
                'get_lower_resolution should return a list of non-empty list')
            self.assertTrue(checker_generic.returns_list_of_Ts(
                lambda x: x, [sublist], int)[0], msg)

    def _returns_list_of_n_ints(self, func: callable, args: list, n: int):
        """Check that func(args) returns a list of n ints."""

        print('\nChecking {}...'.format(func.__name__))
        result = checker_generic.returns_list_of_Ts(func, args, int)
        self.assertTrue(result[0], result[1])

        msg = checker_generic.type_error_message(
            func.__name__, 'list of {} ints'.format(n), result[1])

        self.assertTrue(len(result[1]) == n, msg)
        for i in range(n):
            self.assertTrue(isinstance(result[1][i], int), msg)
        print('  check complete')

    def _check_simple_type(self, func: callable, args: list,
                           expected: type) -> None:
        """Check that func called with arguments args returns a value of type
        expected. Display the progress and the result of the check.

        """

        print('\nChecking {}...'.format(func.__name__))
        result = checker_generic.type_check_simple(func, args, expected)
        self.assertTrue(result[0], result[1])
        print('  check complete')


checker_generic.ensure_no_io('elevation')
TARGET_LEN = 79
print(''.center(TARGET_LEN, "="))
print(' Start: checking coding style '.center(TARGET_LEN, "="))
checker_generic.run_pyta('elevation.py', 'pyta/a2_pyta.txt')
print(' End checking coding style '.center(TARGET_LEN, "="))

print(' Start: checking type contracts '.center(TARGET_LEN, "="))
unittest.main(exit=False)
print(' End checking type contracts '.center(TARGET_LEN, "="))

print('\nScroll up to see ALL RESULTS:')
print('  - checking coding style')
print('  - checking type contract\n')
