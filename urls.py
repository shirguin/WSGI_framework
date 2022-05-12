from datetime import date
from views import Index, Contact, AnotherPage, Examples, Page


# Front Controller
# Исправить на текущий год
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/contact/': Contact(),
    '/another_page/': AnotherPage(),
    '/examples/': Examples(),
    '/page/': Page()
}
