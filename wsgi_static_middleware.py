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


# Response body iterator
def _iter_and_close(file_obj, block_size, charset):
    """Yield file contents by block then close the file."""
    while True:
        try:
            block = file_obj.read(block_size)
            if block:
                yield block.encode(charset)
            else:
                raise StopIteration
        except StopIteration:
            file_obj.close()
            break


def _get_body(filename, method, block_size, charset):
    if method == 'HEAD':
        return [b'']
    return _iter_and_close(open(filename), block_size, charset)


# View functions
def static_file_view(env, start_response, filename, block_size, charset):
    headers = Headers([])

    mimetype, encoding = mimetypes.guess_type(filename)
    headers.add_header('Content-Encodings', encoding)
    headers.add_header('Content-Type', get_content_type(mimetype, charset))
    headers.add_header('Content-Length', get_content_length(filename))
    headers.add_header('Last-Modified', generate_last_modified())
    headers.add_header("Accept-Ranges", "bytes")

    start_response('200 OK', headers.items())
    return _get_body(filename, env['REQUEST_METHOD'].upper(),
                     block_size, charset)


def http404(env, start_response):
    start_response('404 Not Found',
                   [('Content-type', 'text/plain; charset=utf-8')])
    return [b'404 Not Found']


# Middleware class
class StaticMiddleware:
    def __init__(self, app, static_root, static_dirs=None,
                 block_size=16*4096, charset='UTF-8'):
        self.app = app
        self.static_root = static_root.lstrip('/').rstrip('/')
        if static_dirs is None:
            static_dirs = [os.path.join(os.path.abspath('.'), 'static')]
        self.static_dirs = static_dirs
        self.charset = charset
        self.block_size = block_size

    def __call__(self, env, start_response):
        path = env['PATH_INFO'].lstrip('/')
        if path.startswith(self.static_root):
            relative_file_path = '/'.join(path.split('/')[1:])
            return self.handle(env, start_response, relative_file_path)
        return self.app(env, start_response)

    def run(self, *args, **kwargs):
        # For Bottle applications.
        return self.app.run(*args, **kwargs)

    def handle(self, env, start_response, filename):
        abs_file_path = search_file(filename, self.static_dirs)
        if abs_file_path:
            return static_file_view(env, start_response, abs_file_path,
                                    self.block_size, self.charset)
        else:
            return http404(env, start_response)
