from wsgi_framework.templator import render


class Index:
    def __call__(self, request):
        context = {
            'title': 'Главная',
            'request': request
        }
        return '200 OK', render('index.html', context=context, encoding='utf-8')


class Contact:
    def __call__(self, request):
        context = {
            'title': 'Контакты',
            'request': request
        }
        return '200 OK', render('contact.html', context=context, encoding='utf-8')


class AnotherPage:
    def __call__(self, request):
        context = {
            'title': 'Другая страница',
            'request': request
        }
        return '200 OK', render('another_page.html', context=context, encoding='utf-8')


class Examples:
    def __call__(self, request):
        context = {
            'title': 'Примеры',
            'request': request
        }
        return '200 OK', render('examples.html', context=context, encoding='utf-8')


class Page:
    def __call__(self, request):
        context = {
            'title': 'Страница',
            'request': request
        }
        return '200 OK', render('page.html', context=context, encoding='utf-8')
