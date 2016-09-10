import os
import time
import mimetypes
from wsgiref.headers import Headers


# Search File
def is_accessible(abs_file_path):
    return (
        os.path.exists(abs_file_path) and
        os.path.isfile(abs_file_path) and
        os.access(abs_file_path, os.R_OK)
    )


def search_file(relative_file_path, dirs):
    for d in dirs:
        if not os.path.isabs(d):
            d = os.path.abspath(d) + os.sep

        file = os.path.join(d, relative_file_path)
        if is_accessible(file):
            return file


# Header utils
def get_content_length(filename):
    stats = os.stat(filename)
    return str(stats.st_size)


def generate_last_modified():
    last_modified = time.strftime("%a, %d %b %Y %H:%M:%sS GMT", time.gmtime())
    return last_modified


def get_content_type(mimetype, charset):
    if mimetype.startswith('text/') or mimetype == 'application/javascript':
        mimetype += '; charset={}'.format(charset)
    return mimetype


def get_body(filename, method):
    if method == 'HEAD':
        body = b''
    else:
        with open(filename, 'rb') as f:
            body = f.read()
    return body


# View functions
def static_file_view(env, start_response, filename, charset):
    method = env['REQUEST_METHOD'].upper()
    headers = Headers()

    mimetype, encoding = mimetypes.guess_type(filename)
    headers.add_header('Content-Encodings', encoding)
    headers.add_header('Content-Type', get_content_type(mimetype, charset))
    headers.add_header('Content-Length', get_content_length(filename))
    headers.add_header('Last-Modified', generate_last_modified())
    headers.add_header("Accept-Ranges", "bytes")

    body = get_body(filename, method)
    start_response('200 OK', headers.items())
    return [body]


def http404(env, start_response):
    start_response('404 Not Found', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'404 Not Found']


# Middleware class
class StaticMiddleware:
    def __init__(self, app, static_root, static_dirs, charset='UTF-8'):
        self.app = app
        self.static_root = static_root
        self.static_dirs = static_dirs
        self.charset = charset

    def __call__(self, env, start_response):
        path = env['PATH_INFO'].lstrip('/')
        if path.startswith(self.static_root):
            relative_file_path = '/'.join(path.split('/')[1:])
            return self.handle(env, start_response, relative_file_path)
        return self.app(env, start_response)

    def handle(self, env, start_response, filename):
        abs_file_path = search_file(filename, self.static_dirs)
        if abs_file_path:
            return static_file_view(env, start_response, abs_file_path, self.charset)
        else:
            return http404(env, start_response)
