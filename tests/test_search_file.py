import os
from unittest import TestCase

from wsgi_static_middleware import (
    is_accessible,
    search_file,
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
STATIC_DIRS = [STATIC_DIR]


class IsAccessibleTests(TestCase):
    def test_is_accessible(self):
        file_path = os.path.join(STATIC_DIR, 'app.js')
        self.assertTrue(is_accessible(file_path))

    def test_is_not_accessible(self):
        file_path = os.path.join(STATIC_DIR, 'no-exists.js')
        self.assertFalse(is_accessible(file_path))


class SearchFileTests(TestCase):
    def test_return_abs_file_path(self):
        actual_file_path = search_file('app.js', STATIC_DIRS)
        self.assertIsInstance(actual_file_path, str)

    def test_is_not_accessible(self):
        actual_file_path = search_file('no-exists.js', STATIC_DIRS)
        self.assertIsNone(actual_file_path)
