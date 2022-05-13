from datetime import date
from views import Index, Contact, AnotherPage, Examples, Page


# Front Controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


def csslink(request):
    request['csslink'] = '/static/style.css'


fronts = [secret_front, other_front, csslink]

routes = {
    '/': Index(),
    '/contact/': Contact(),
    '/another_page/': AnotherPage(),
    '/examples/': Examples(),
    '/page/': Page()
}
