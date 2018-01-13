from jinja2 import Environment, FileSystemLoader
import os.path
from utils import log



path = '{}/templates/'.format(os.path.dirname(__file__))
log('path, ', path)
loader = FileSystemLoader(path)
env = Environment(loader=loader)


def jinja(path, **args):
    template = env.get_template(path)
    return template.render(**args)


def __main():
    path = 'test.html'
    log(jinja(path, userlist={'name': 'vince', 'age': 19}, title='这是一个标题'))


__main()

