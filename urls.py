from datetime import date



# Front Controller
def current_date(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [current_date, other_front]

# Перенес в views с применением декоратора для контроллеров
# routes = {
#     '/': Index(),
#     '/contact/': Contact(),
#     '/another_page/': AnotherPage(),
#     '/users/': Users(),
#     '/page/': Page(),
#     '/create-category/': CreateCategory(),
#     '/courses-list/': CoursesList(),
#     '/create-course/': CreateCourse(),
#     '/copy-course/': CopyCourse(),
#     '/create_user/': CreateUser()
# }
