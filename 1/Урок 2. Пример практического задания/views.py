from simba_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))


class About:
    # {'method': 'GET', 'request_params': {'id': '1', 'category': '10'}}
    def __call__(self, request):
        return '200 OK', 'about'
