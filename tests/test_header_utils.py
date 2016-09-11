import os
from unittest import TestCase
import mimetypes

from wsgi_static_middleware import (
    get_content_length,
    get_content_type,
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')


class HeaderUtilsTests(TestCase):
    def test_get_content_length(self):
        file_path = os.path.join(STATIC_DIR, 'app.js')
        actual = get_content_length(file_path)
        expected_content_length = '28'
        self.assertEqual(actual, expected_content_length)

    def test_get_content_type_set_utf8_to_js(self):
        file_path = os.path.join(STATIC_DIR, 'app.js')
        mimetype, encoding = mimetypes.guess_type(file_path)
        actual = get_content_type(mimetype, charset='UTF-8')
        expected = 'application/javascript; charset=UTF-8'
        self.assertEqual(actual, expected)

    def test_get_content_type_set_utf8_to_css(self):
        file_path = os.path.join(STATIC_DIR, 'style.css')
        mimetype, encoding = mimetypes.guess_type(file_path)
        actual = get_content_type(mimetype, charset='UTF-8')
        expected = 'text/css; charset=UTF-8'
        self.assertEqual(actual, expected)

    def test_get_content_type_does_not_set_utf8(self):
        file_path = os.path.join(STATIC_DIR, 'kobin.png')
        mimetype, encoding = mimetypes.guess_type(file_path)
        actual = get_content_type(mimetype, charset='UTF-8')
        expected = 'image/png'
        self.assertEqual(actual, expected)
