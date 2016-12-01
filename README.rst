wsgi-static-middleware
======================

.. image:: https://travis-ci.org/kobinpy/wsgi-static-middleware.svg?branch=master
    :target: https://travis-ci.org/kobinpy/wsgi-static-middleware

.. image:: https://badge.fury.io/py/wsgi-static-middleware.svg
    :target: https://badge.fury.io/py/wsgi-static-middleware

WSGI Middleware for serving static files.

Usage
-----

.. code-block:: python

   import os
   from wsgiref.simple_server import make_server
   from wsgi_static_middleware import StaticMiddleware
   
   BASE_DIR = os.path.dirname(__name__)
   STATIC_DIRS = [os.path.join(BASE_DIR, 'static')]
   
   
   def app(env, start_response):
       start_response('200 OK', [('Conte-type', 'text/plain; charset=utf-8')])
       return [b'Hello World']
   
   app = StaticMiddleware(app, static_root='static', static_dirs=STATIC_DIRS)
   
   if __name__ == '__main__':
       httpd = make_server('', 8000, app)
       httpd.serve_forever()


.. code-block:: bash

   $ curl -v localhost:8000/static/style.css
   *   Trying ::1...
   * connect to ::1 port 8000 failed: Connection refused
   *   Trying 127.0.0.1...
   * Connected to localhost (127.0.0.1) port 8000 (#0)
   > GET /static/style.css HTTP/1.1
   > Host: localhost:8000
   > User-Agent: curl/7.43.0
   > Accept: */*
   >
   * HTTP 1.0, assume close after body
   < HTTP/1.0 200 OK
   < Date: Sun, 11 Sep 2016 03:42:33 GMT
   < Server: WSGIServer/0.2 CPython/3.5.1
   < Content-Encodings:
   < Content-Type: text/css; charset=UTF-8
   < Content-Length: 30
   < Last-Modified: Sun, 11 Sep 2016 03:42:1473532953S GMT
   < Accept-Ranges: bytes
   <
   .foo {
       font-size: 10px;
   }
   * Closing connection 0


LICENSE
-------

::

   MIT License
   
   Copyright (c) 2016 Masashi SHIBATA
   
   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:
   
   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.
   
   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.

