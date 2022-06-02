from copy import deepcopy
from quopri import decodestring
from sqlite3 import connect

from patterns.architectural_system_pattern_unit_of_work import DomainObject
from patterns.behavioral_patterns import Subject, FileWriter

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
class Student(User, DomainObject):
    def __init__(self, surname, name, patronymic, age):
        self.type_user = 'student'
        self.courses = []
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


class Course(CoursePrototype, Subject):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


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
        # self.users = []

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

    def get_student(self, surname) -> Student:
        for item in self.students:
            if item.surname == surname:
                return item

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

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)


class StudentMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.table_name = 'student'

    def all(self):
        statement = f'SELECT * from {self.table_name}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, surname, name, patronymic, age = item
            student = Student(surname, name, patronymic, age)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f'SELECT id, name FROM {self.table_name} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        # statement = f'INSERT INTO {self.table_name} (name) VALUES (?)'
        # self.cursor.execute(statement, (obj.name, ))
        statement = f'INSERT INTO {self.table_name} (surname, name, patronymic, age) VALUES (?, ?, ?, ?)'
        self.cursor.execute(statement, (obj.surname, obj.name, obj.patronymic, obj.age, ))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f'UPDATE {self.table_name} SET name=? WHERE id=?'
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = connect('patterns.sqlite')

'''Архитектурный системный паттерн - Data Mapper'''


class MapperRegistry:
    mappers = {
        'student': StudentMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')
