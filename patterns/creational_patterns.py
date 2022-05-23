from copy import deepcopy
from quopri import decodestring


# Клас абстрактного пользователя
class User:
    pass


# Класс преподователя
class Teacher(User):
    pass


# Класс студента
class Student(User):
    pass


# Класс создания пользователей
class UserFactory:
    types_users = {
        'teacher': Teacher,
        'student': Student
    }

    # Создаем пользователя (Фабричный метод)
    @classmethod
    def create(cls, type_user):
        return cls.types_users[type_user]()


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

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.curse_count()
        return result

# Проверка работы класов
# st = UserFactory.create('student')
# print(type(st), st)
# th = UserFactory.create('teacher')
# print(type(th), th)

cat_1 = Category('Программирование', None)
print(type(cat_1), cat_1)
print(cat_1.id, cat_1.name)
cat_2 = Category('Анализ данных', None)
print(type(cat_2), cat_2)
print(cat_2.id, cat_2.name)

# course_1 = CourseFactory.create('interactive', 'Python', 'Программирование')
# print(type(course_1), course_1)
