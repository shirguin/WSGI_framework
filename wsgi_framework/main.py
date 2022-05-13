from wsgi_framework.templator import render


class Framework:
    def __init__(self, routes_obj_ls, fronts_obj_ls):
        self.lsRoutes = routes_obj_ls
        self.lsFronts = fronts_obj_ls

    def __call__(self, environ, start_response):
        method = environ['REQUEST_METHOD']
        query_string = environ['QUERY_STRING']
        print(f'Метод запроса:{method}:{query_string}')

        request_params = self.parse_input_data(query_string)
        print(f'Список Request_Params: {request_params}')

        # Адрес перехода
        path = environ['PATH_INFO']

        # Проверка на наличие закрывающего слеша
        if not path.endswith('/'):
            path += '/'

        # отработка паттерна Page Controller
        if path in self.lsRoutes:
            view = self.lsRoutes[path]
        else:
            view = PageNotFound404()

        # Отработка паттерна Front Controller
        request = {}
        for front in self.lsFronts:
            front(request)

        # Передаем словарь request  в контроллер и запускаем его
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    def parse_input_data(self, data: str):
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                key, value = item.split('=')
                result[key] = value
        return result


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', render('404.html')

