from datetime import date
from views import Index, Contact, AnotherPage, Examples, Page, CreateCategory


# Front Controller
def current_date(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [current_date, other_front]

routes = {
    '/': Index(),
    '/contact/': Contact(),
    '/another_page/': AnotherPage(),
    '/examples/': Examples(),
    '/page/': Page(),
    '/create-category/': CreateCategory(),
}
