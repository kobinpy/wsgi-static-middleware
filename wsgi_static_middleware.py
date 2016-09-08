import os
import time
import mimetypes
from wsgiref.headers import Headers


def http404(env, start_response):
    start_response('404 Not Found', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'404 Not Found']


def get_last_modified():
    last_modified = time.strftime("%a, %d %b %Y %H:%M:%sS GMT", time.gmtime())
    return 'Last-Modified', last_modified


def get_content_length(filename):
    stats = os.stat(filename)
    return 'Content-Length', str(stats.st_size)


def get_body(filename, method):
    if method == 'HEAD':
        body = b''
    else:
        with open(filename, 'rb') as f:
            body = f.read()
    return body


class StaticMiddleware:
    default_charset = 'UTF-8'

    def __init__(self, app, static_root, static_dirs, download=''):
        self.app = app
        self.static_root = static_root
        self.static_dirs = static_dirs
        self.download = download

    def __call__(self, env, start_response):
        path = env['PATH_INFO'].lstrip('/')
        if path.startswith(self.static_root):
            relative_file_path = '/'.join(path.split('/')[1:])
            return self.handle(env, start_response, relative_file_path)
        return self.app(env, start_response)

    def get_abs_file_path(self, relative_file_path):
        for directory in self.static_dirs:
            if not os.path.isabs(directory):
                directory = os.path.abspath(directory) + os.sep
            file = os.path.join(directory, relative_file_path)
            if os.path.exists(file) and os.path.isfile(file) and os.access(file, os.R_OK):
                if os.access(file, os.R_OK):
                    return file

    def handle(self, env, start_response, filename):
        abs_file_path = self.get_abs_file_path(filename)
        if abs_file_path:
            return self.static_file_view(env, start_response, abs_file_path)
        else:
            return http404(env, start_response)

    def static_file_view(self, env, start_response, filename):
        method = env['REQUEST_METHOD'].upper()
        headers = Headers()

        mimetype, encoding = mimetypes.guess_type(self.download if self.download else filename)
        if encoding:
            headers.add_header('Content-Encodings', encoding)
        if mimetype:
            if ((mimetype.startswith('text/') or mimetype == 'application/javascript')
                    and 'charset' not in mimetype):
                mimetype += '; charset={}'.format(self.default_charset)
            headers.add_header('Content-Type', mimetype)

        headers.add_header(*get_content_length(filename))
        headers.add_header(*get_last_modified())
        headers.add_header("Accept-Ranges", "bytes")

        body = get_body(filename, method)
        start_response('200 OK', headers.items())
        return [body]
