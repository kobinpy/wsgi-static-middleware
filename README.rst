wsgi-static-middleware
======================

Basic static file serving middleware for WSGI.

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

   $ curl localhost:8000/static/style.css
   .foo {
       font-size: 10px;
   }


LICENSE
-------

MIT License
