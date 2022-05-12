from wsgiref.simple_server import make_server


def application(environ, start_response):
    path = environ['PATH_INFO']
    if path == '/':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Index']
    elif path == '/adidas/':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'adidas']
    else:
        start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
        return [b'404 not Found']


with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
