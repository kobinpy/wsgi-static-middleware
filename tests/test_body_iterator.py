import os
from unittest import TestCase

from wsgi_static_middleware import (
    _get_body,
    _iter_and_close,
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')


class IterAndCloseTests(TestCase):
    def test_get_body_returns_empty_body_when_catch_head_request(self):
        file_path = os.path.join(STATIC_DIR, 'style.css')
        actual = _get_body(file_path, 'HEAD', 16*4096, 'UTF-8')
        expected = [b'']
        self.assertEqual(actual, expected)

    def test_iter_and_close(self):
        file_path = os.path.join(STATIC_DIR, 'app.js')
        actual = list(_iter_and_close(open(file_path), 10, 'UTF-8'))
        expected = [
            b"console.lo",
            b"g('Hello W",
            b"orld');\n"
        ]
        self.assertEqual(actual, expected)
