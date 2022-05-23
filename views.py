from patterns.creational_patterns import Engine
from wsgi_framework.templator import render

site = Engine()

class Index:
    def __call__(self, request):
        context = {
            'title': 'Главная',
            'request': request,
            'categories': site.categories
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


# Создать категорию
class CreateCategory:
    def __call__(self, request):
        if request['method'] == 'POST':
            pass
            # data = request['data']
            # name_category = data['name_category']
            # name_category = site.decode_value(name_category)
            #
            # category_id = data.get('category_id')
            #
            # category = None
            # if category_id:
            #     category = site.find_category_by_id(int(category_id))
            #
            # new_category = site.create_category(name_category)
            # site.categories.append(new_category)
            # return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)
