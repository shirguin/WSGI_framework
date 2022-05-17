from wsgi_framework.requests import Requests
from wsgi_framework.templator import render


class Framework:
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
        request[method] = method
        if method == 'GET':
            request_params = Requests().get_Get_request_params(environ)
            request['request_params'] = request_params
            print(f'Получены GET-параметры: {request_params}')

        if method =='POST':
            data = Requests().get_Post_request_params(environ)
            request['data'] = data
            print(f'Получен POST-запрос: {data}')

        # отработка паттерна Page Controller
        if path in self.lsRoutes:
            view = self.lsRoutes[path]
        else:
            view = PageNotFound404()

        # Отработка паттерна Front Controller
        for front in self.lsFronts:
            front(request)

        # Передаем словарь request  в контроллер и запускаем его
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    # def parse_input_data(self, data: str):
    #     result = {}
    #     if data:
    #         params = data.split('&')
    #         for item in params:
    #             key, value = item.split('=')
    #             result[key] = value
    #     return result


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', render('404.html')

