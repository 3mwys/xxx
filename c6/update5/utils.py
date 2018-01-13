from jinja2 import Environment, FileSystemLoader
import os.path
import time


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    file = 'vin.log.txt'
    with open(file, 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


path = '{}/templates/'.format(os.path.dirname(__file__))
log('path, ', path)
loader = FileSystemLoader(path)
env = Environment(loader=loader)


def template(path, **args):
    t = env.get_template(path)
    return t.render(**args)




