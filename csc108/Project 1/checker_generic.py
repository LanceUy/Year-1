"""Runner for assignment sanity checkers, including PyTA.
"""

import sys
from typing import Tuple


def ensure_no_io(modulename: str) -> None:
    """Mock built-in functions input and print, so that they raise
    exceptions.

    """

    test_module = sys.modules[modulename]
    setattr(test_module, "input", _mock_disallow("input"))
    setattr(test_module, "print", _mock_disallow("print"))


def run_pyta(filename: str, config_file: str) -> None:
    """Run PYTA with configuration config_file on the file named filename.

    """

    sys.path.insert(0, 'pyta')
    import python_ta
    python_ta.check_all(filename, config=config_file)


def check(func: callable, args: list,
          expected: type) -> Tuple[bool, str]:
    """Check if func(args) returns a result of type expected.

    Return (True, result-of-call) if the check succeeds.
    Return (False, error-or-failure-message) if anything goes wrong.
    """

    try:
        returned = func(*args)
    except Exception as exn:
        return (False, _error_message(func, args, exn))

    if isinstance(returned, expected):
        return (True, returned)

    return (False, _type_error_message(func, expected, returned))


def _type_error_message(func: callable, expected: type,
                        got: object) -> str:
    """Return an error message for function func returning got, where the
    correct return type is expected.

    """

    return ('{} should return a {}, but returned {}' +
            '.').format(func.__name__, expected.__name__, got)


def _error_message(func: callable, args: list,
                   error: Exception) -> str:
    """Return an error message: func(args) raised an error."""

    return 'The call {}({}) caused an error: {}'.format(
        func.__name__, ','.join(map(str, args)), error)


def _mock_disallow(func_name: str):
    """Raise an Exception saying that use of function func_name is not
    allowed.

    """

    raise Exception("The use of function {} is not allowed.".format(func_name))
