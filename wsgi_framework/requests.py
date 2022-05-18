class GetRequests:
    # Парсер данных
    @staticmethod
    def parse_input_data(data: str):
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                key, value = item.split('=')
                result[key] = value
        return result

    # Метод получения параметров GET запроса
    @staticmethod
    def get_request_params(environ):
        query_string = environ['QUERY_STRING']
        request_params = GetRequests.parse_input_data(query_string)
        return request_params


class PostRequests:
    # Парсер данных
    @staticmethod
    def parse_input_data(data: str):
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                key, value = item.split('=')
                result[key] = value
        return result

    # Получаем данные POST запроса в bytes
    @staticmethod
    def get_wsgi_input_data(environ) -> bytes:
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        print(f'Длина полученных данных: {content_length} байт')
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    # Парсер данных в bytes
    def parse_wsgi_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            # декодируем данные
            data_str = data.decode(encoding="utf-8")
            print(f'Строка данных после декодирования: {data_str}')
            # собираем их в словарь
            result = self.parse_input_data(data_str)
        return result

    # Метод получения данных POST запроса
    def get_request_params(self, environ):
        # получаем данные
        data = self.get_wsgi_input_data(environ)
        # превращаем данные в словарь
        data = self.parse_wsgi_input_data(data)
        return data
