"""Utilities for tests."""

import inspect
from functools import wraps
from unittest import mock


def mock_envs(**envs):
    """Mock environment variables for test.

    Can be applied to:
      - any function
      - test class - all test methods (starts with "test_*" will be decorated)
    """

    def decorator(obj):
        @wraps(obj)
        def wrapper(*args, **kwargs):
            with mock.patch.dict('os.environ', envs, clear=True):
                obj(*args, **kwargs)

        if inspect.isclass(obj):
            for name, method in inspect.getmembers(obj, inspect.isfunction):
                if name.startswith('test_'):
                    setattr(obj, name, decorator(method))
            return obj
        else:
            return wrapper

    return decorator