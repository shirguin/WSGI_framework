from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    env = Environment()
    #Указываем папку для поиска шаблонов и подшаблонов(все будет в одном месте)
    env.loader = FileSystemLoader(folder)
    #Находим шаблон в окружении
    template = env.get_template(template_name)
    return template.render(**kwargs)
