from quopri import decodestring

from wsgi_framework.requests import GetRequests, PostRequests
from wsgi_framework.templator import render


class Framework:
    """Класс Framework - основа фреймворка"""
    def __init__(self, routes_obj_ls, fronts_obj_ls):
        self.lsRoutes = routes_obj_ls
        self.lsFronts = fronts_obj_ls

    def __call__(self, environ, start_response):
        # Адрес перехода
        path = environ['PATH_INFO']

        # Проверка на наличие закрывающего слеша
        if not path.endswith('/'):
            path += '/'

        request = {}
        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = Framework.decode_value(request_params)
            print(f'Получены GET-параметры: {Framework.decode_value(request_params)}')

        if method =='POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = Framework.decode_value(data)
            print(f'Получен POST-запрос: {Framework.decode_value(data)}')

        # находим нужный контроллер
        # отработка паттерна Page Controller
        if path in self.lsRoutes:
            view = self.lsRoutes[path]
            content_type = self.get_content_type(path)
            code, body = view(request)
            body = body.encode('utf-8')

        elif path.startswith(self.settings.STATIC_URL):

        else:
            view = PageNotFound404()

        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # Отработка паттерна Front Controller
        for front in self.lsFronts:
            front(request)

        # Передаем словарь request  в контроллер и запускаем его
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    # Декодер данных
    @staticmethod
    def decode_value(data):
        new_data = {}
        for key, value in data.items():
            val = bytes(value.replace("%", "=").replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[key] = val_decode_str
        return new_data


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', render('404.html')

