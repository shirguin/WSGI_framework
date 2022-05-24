from copy import deepcopy
from quopri import decodestring


# Класс абстрактного пользователя
class User:
    def __init__(self, surname, name, patronymic, age):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.age = age


# Класс преподователя
class Teacher(User):
    def __init__(self, surname, name, patronymic, age):
        self.type_user = 'teacher'
        super().__init__(surname, name, patronymic, age)


# Класс студента
class Student(User):
    def __init__(self, surname, name, patronymic, age):
        self.type_user = 'student'
        super().__init__(surname, name, patronymic, age)


# Класс создания пользователей
class UserFactory:
    types_users = {
        'teacher': Teacher,
        'student': Student
    }

    # Создаем пользователя (Фабричный метод)
    @classmethod
    def create(cls, surname, name, patronymic, age, type_user):
        return cls.types_users[type_user](surname, name, patronymic, age)


# Порождающий паттерн Прототип (прототив курсов обучения)
class CoursePrototype:
    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


# Клас интерактивного курса
class InteractiveCourse(Course):
    pass


# Клас курса в записи
class RecordCourse(Course):
    pass


# Клас создания курса
class CourseFactory:
    types_course = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    # Создание курса (Фабричный метод)
    @classmethod
    def create(cls, type_course, name, category):
        return cls.types_course[type_course](name, category)


# Класс категории
class Category:
    auto_id = 0

    def __init__(self, name_category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.category = name_category
        self.courses = []

    def course_count(self):
        return len(self.courses)


# Основной интерфейс проекта
class Engine:
    def __init__(self):
        self.students = []
        self.teachers = []
        self.courses = []
        self.categories = []
        self.users = []

    @staticmethod
    def create_user(surname, name, patronymic, age, type_user):
        user = UserFactory.create(surname, name, patronymic, age, type_user)
        return user

    @staticmethod
    def create_category(name_category):
        return Category(name_category)

    def find_category_by_id(self, id):
        for item in self.categories:
            if item.id == id:
                return item
        raise Exception(f'Категории с id = {id} не существует')

    @staticmethod
    def create_course(type_course, name, category):
        return CourseFactory.create(type_course, name, category)

    def get_course(self, name_course):
        for item in self.courses:
            if item.name == name_course:
                return item
        return None

    @staticmethod
    def decode_value(value):
        value_b = bytes(value.replace('%', '=').replace("+", " "), 'utf-8')
        value_decode_str = decodestring(value_b)
        return value_decode_str.decode('utf-8')


# Порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)
