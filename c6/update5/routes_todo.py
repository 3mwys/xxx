from utils import log
from utils import template
from todo import Todo
from models import User
from routes import current_user
import time


def response_http(body):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def response_with_headers(headers, code=200):
    header = 'HTTP/1.1 {} VERY OK\r\n'.format(code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                           for k, v in headers.items()])
    return header


def redirect(url):
    headers = {
        'Location': url,
    }
    r = response_with_headers(headers, 302) + '\r\n'
    return r.encode('utf-8')


def login_required(route_function):
    def f(request):
        uname = current_user(request)
        u = User.find_by(username=uname)
        if u is None:
            return redirect('/login')
        return route_function(request)
    return f


def look_time():
    format = '%m/%d %H:%M'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    return dt


def index(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    todo_list = Todo.find_all(user_id=u.id)
    body = template('jinja_test.html', user_list=todo_list)
    log('这是 body:', body)
    return response_http(body)


def edit(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    log('这是reqeust', request.query)
    todo_id = int(request.query.get('id', -1))
    log('todo_id', todo_id)
    t = Todo.find_by(id=todo_id)
    log('** 这是t:', t)
    if t.user_id != u.id:
        return redirect('/login')
    body = template('jinja_test_edit.html', user=t)
    return response_http(body)


def add(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if request.method == 'POST':
        form = request.form()
        t = Todo.new(form)
        t.created_time = look_time()
        t.updated_time = look_time()
        log('*** time:', t.created_time)
        t.user_id = u.id
        t.save()
    return redirect('/todo')


def update(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    if request.method == 'POST':
        form = request.form()
        print('debug update', form)
        todo_id = int(form.get('id', -1))
        t = Todo.find_by(id=todo_id)
        t.updated_time = look_time()
        t.title = form.get('title', t.title)
        t.save()
    return redirect('/todo')


def delete_todo(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    if t.user_id != u.id:
        return redirect('/login')
    if t is not None:
        t.remove()
    return redirect('/todo')

# admin 的 template 还没有换
def user_admin(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u.role != 1:
        return redirect('/login')
    todo_list = User.all()
    body = template('admin.html', user_list=todo_list)
    return response_http(body)


def user_update(request):
    if request.method == 'POST':
        form = request.form()
        print('debug update', form)
        todo_id = int(form.get('id', -1))
        u = User.find_by(id=todo_id)
        u.password = form.get('password', u.password)
        u.save()
    return redirect('/admin/users')


route_dict = {
    # GET 请求, 显示页面
    '/todo': index,
    '/todo/edit': login_required(edit),
    # POST 请求, 处理数据
    '/todo/add': login_required(add),
    '/todo/update': login_required(update),
    '/todo/delete': delete_todo,
    '/admin/users': login_required(user_admin),
    '/admin/user/update': login_required(user_update),
}
