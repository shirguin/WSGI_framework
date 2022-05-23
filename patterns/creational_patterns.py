from copy import deepcopy
from quopri import decodestring


# Клас абстрактного пользователя
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
        result = len(self.courses)
        if self.category:
            result += self.category.curse_count()
        return result


# Основной интерфейс проекта
class Engine:
    def __init__(self):
        self.students = []
        self.teachers = []
        self.courses = []
        self.categories = []

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
    def decode_value(value):
        value_b = bytes(value.replace('%', '=').replace("+", " "), 'utf-8')
        value_decode_str = decodestring(value_b)
        return value_decode_str.decode('utf-8')


# Проверка работы Engine
# site = Engine()
#
# st_1 = site.create_user('Иванов', 'Иван', 'Иванович', 22, 'student')
# site.students.append(st_1)
# st_2 = site.create_user('Петров', 'Петр', 'Петрович', 21, 'student')
# site.students.append(st_2)
# for st in site.students:
#     print(st.surname, st.name, st.patronymic, st.age, st.type_user)
#
# th_1 = site.create_user('Семенов', 'Иван', 'Иванович', 22, 'teacher')
# site.teachers.append(th_1)
# th_2 = site.create_user('Кирилов', 'Петр', 'Петрович', 21, 'teacher')
# site.teachers.append(th_2)
# for th in site.teachers:
#     print(th.surname, th.name, th.patronymic, th.age, th.type_user)

# cat_1 = site.create_category('Программирование')
# print(cat_1.id, cat_1.category, cat_1.courses)
