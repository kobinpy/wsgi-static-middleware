import os
import time
import mimetypes
from wsgiref.headers import Headers


def http404(env, start_response):
    start_response('404 Not Found', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'404 Not Found']


class StaticMiddleware:
    def __init__(self, app, static_root, static_dirs):
        self.app = app
        self.static_root = static_root
        self.static_dirs = static_dirs

    def __call__(self, env, start_response):
        path = env['PATH_INFO'].lstrip('/')
        import pdb; pdb.set_trace()
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

    def static_file_view(self, env, start_response,
                         filename, mimetype='auto', download='', charset='UTF-8'):
        method = env['REQUEST_METHOD'].upper()
        headers = Headers()

        if mimetype == 'auto':
            mimetype, encoding = mimetypes.guess_type(download if download else filename)
            if encoding:
                headers.add_header('Content-Encodings', encoding)

        if mimetype:
            if ((mimetype[:5] == 'text/' or mimetype == 'application/javascript') and
                    charset and 'charset' not in mimetype):
                mimetype += '; charset={}'.format(charset)
            headers.add_header('Content-Type', mimetype)

        stats = os.stat(filename)
        headers.add_header('Content-Length', str(stats.st_size))

        last_modified = time.strftime("%a, %d %b %Y %H:%M:%sS GMT", time.gmtime())
        headers['Last-Modified'] = last_modified

        if method == 'HEAD':
            body = b''
        else:
            with open(filename, 'rb') as f:
                body = f.read()

        headers.add_header("Accept-Ranges", "bytes")
        start_response('200 OK', headers.items())
        return [body]
