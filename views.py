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
            print('IF POST')
            data = request['data']
            name_category = data['name_category']
            name_category = site.decode_value(name_category)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name_category)
            site.categories.append(new_category)

            context = {
                'title': 'Главная',
                'request': request,
                'categories': site.categories
            }
            return '200 OK', render('index.html', context=context, encoding='utf-8')
        else:
            context = {
                'title': 'Создание категории',
                'request': request,
                'categories': site.categories
            }
            return '200 OK', render('create_category.html', context=context)


# Список курсов
class CoursesList:
    def __call__(self, request):
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            context = {
                'title': 'Список курсов',
                'request': request,
                'objects_list': category.courses,
                'category': category.category,
                'id': category.id
            }
            return '200 OK', render('course-list.html', context=context)
        except KeyError:
            return '200 OK', 'Курсы еще не добавлены'


# Создать курс
class CreateCourse:
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name_course = data['name_course']
            name_course = site.decode_value(name_course)

            category = site.find_category_by_id(int(self.category_id))

            course = site.create_course('interactive', name_course, category)
            site.courses.append(course)
            context = {
                'title': 'Список курсов',
                'request': request,
                'objects_list': category.courses,
                'category': category.category,
                'id': category.id
            }
            return '200 OK', render('course-list.html', context=context)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))
                context = {
                    'title': 'Создание курса',
                    'request': request,
                    'category': category.category,
                    'id': category.id
                }
                return '200 OK', render('create-course.html', context=context)
            except KeyError:
                return '200 OK', 'Категории еще не добавлены'


# Список категорий
class CategoryList:
    pass


# Копирование курса
class CopyCourse:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name_course = request_params['name_course']
            old_course = site.get_course(name_course)
            category = old_course.category
            if old_course:
                new_name_course = f'copy_{name_course}'
                new_course = old_course.clone()
                new_course.name = new_name_course
                site.courses.append(new_course)
                new_course.category.courses.append(new_course)
                context = {
                    'title': 'Список курсов',
                    'request': request,
                    'categories': site.categories,
                    # 'objects_list': category.courses,
                    'objects_list': site.courses,
                    'category': category,
                    'id': category.id
                }
                return '200 OK', render('course-list.html', context=context)

        except KeyError:
            return '200 Ok', 'Курсы еще не добавлены'

