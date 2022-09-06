from wsgiref.simple_server import make_server

from wsgi_framework.main import Framework
from urls import fronts
from views import routes
from patterns import settings


application = Framework(routes, fronts, settings)

with make_server('', 8000, application) as httpd:
    print('Сервер запущен на порту 8000...')
    httpd.serve_forever()
