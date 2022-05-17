from quopri import decodestring


class Requests:
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

    # Декодер данных
    @staticmethod
    def decode_value(data):
        new_data = {}
        for key, value in data.items():
            val = bytes(value.replace("%", "=").replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[key] = val_decode_str
        return new_data

    # Метод получения параметров GET запроса
    @staticmethod
    def get_Get_request_params(environ):
        query_string = environ['QUERY_STRING']
        request_params = Requests.parse_input_data(query_string)
        return Requests.decode_value(request_params)

    # Метод получения данных POST запроса
    def get_Post_request_params(self, environ):
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)
        return Requests.decode_value(data)

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
            data_str = data.decode(encoding="utf-8")
            print(f'Строка данных после декодирования: {data_str}')
            print(type(data_str))
            result = self.parse_input_data(data_str)
        return result
