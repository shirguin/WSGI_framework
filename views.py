from patterns.behavioral_patterns import ListView, CreateView
from patterns.creational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug
from wsgi_framework.templator import render


site = Engine()
logger = Logger('main')
routes = {}


@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        logger.log('Категории')
        context = {
            'title': 'Категории',
            'request': request,
            'categories': site.categories
        }
        return '200 OK', render('index.html', context=context, encoding='utf-8')


@AppRoute(routes=routes, url='/contact/')
class Contact:
    @Debug(name='Contact')
    def __call__(self, request):
        logger.log('Контакты')
        context = {
            'title': 'Контакты',
            'request': request
        }
        return '200 OK', render('contact.html', context=context, encoding='utf-8')


@AppRoute(routes=routes, url='/another_page/')
class AnotherPage:
    @Debug(name='AnotherPage')
    def __call__(self, request):
        logger.log('Другая страница')
        context = {
            'title': 'Другая страница',
            'request': request
        }
        return '200 OK', render('another_page.html', context=context, encoding='utf-8')


# @AppRoute(routes=routes, url='/students/')
# class Students:
#     @Debug(name='Users')
#     def __call__(self, request):
#         logger.log('Студенты')
#         context = {
#             'title': 'Студенты',
#             'request': request,
#             'objects_list': site.users
#         }
#         return '200 OK', render('students.html', context=context, encoding='utf-8')


@AppRoute(routes=routes, url='/page/')
class Page:
    @Debug(name='Page')
    def __call__(self, request):
        logger.log('Страница')
        context = {
            'title': 'Страница',
            'request': request
        }
        return '200 OK', render('page.html', context=context, encoding='utf-8')


# Создать категорию
@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    @Debug(name='CreateCategory')
    def __call__(self, request):
        logger.log('Создание категории')

        if request['method'] == 'POST':
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
@AppRoute(routes=routes, url='/courses-list/')
class CoursesList:
    @Debug(name='CoursesList')
    def __call__(self, request):
        logger.log('Список курсов')
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
@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    @Debug(name='CreateCourse')
    def __call__(self, request):
        logger.log('Создание курса')

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


# Копирование курса
@AppRoute(routes=routes, url='/copy-course/')
class CopyCourse:
    @Debug(name='CopyCourse')
    def __call__(self, request):
        logger.log('Копирование курса')
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
                category.courses.append(new_course)
                context = {
                    'title': 'Список курсов',
                    'request': request,
                    'categories': site.categories,
                    'objects_list': category.courses,
                    'category': category.category,
                    'id': category.id
                }
                return '200 OK', render('course-list.html', context=context)

        except KeyError:
            return '200 Ok', 'Курсы еще не добавлены'


@AppRoute(routes=routes, url='/students/')
class StudentListView(ListView):
    queryset = {
        'objects_list': site.students,
        'title': 'Студенты'
    }
    template_name = 'students.html'


@AppRoute(routes=routes, url='/create_student/')
class StudentCreateView(CreateView):
    queryset = {
        'title': 'Регистрация студента'
    }
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        surname = data['surname']
        surname = site.decode_value(surname)

        name = data['name']
        name = site.decode_value(name)

        patronymic = data['patronymic']
        patronymic = site.decode_value(patronymic)

        age = data['age']
        age = site.decode_value(age)

        new_obj = site.create_user(surname, name, patronymic, age, 'student')
        site.students.append(new_obj)

