from data import db_session
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import sqlalchemy.orm as orm
from data.users import User
from data.login_form import LoginForm
from forms.user import RegisterForm
import pymorphy3

from tasks.level_1 import l1_task_1, l1_task_2, l1_task_3
from tasks.level_2 import l2_task_1
from tasks.level_3 import l3_task_1, l3_task_2, l3_task_3

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
SqlAlchemyBase = orm.declarative_base()
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init('db/blogs.db')
    app.run()


@app.route('/')
def main_window():
    return redirect('/basic')


@app.route('/basic')
def basic():
    return render_template('basic.html', title='Поставьте пожалуйста 100 баллов')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Данный nickname уже занят")
        user = User(
            name=form.name.data,
            email=form.email.data,
            check_password=form.password.data,
            progress=0,
            photo='',
            lst_complete_task=''
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        user.photo = f'/static/User_profile_img/user{user.id}.jpg'
        with open(f'static/User_profile_img/user{user.id}.jpg', 'wb') as img:
            img.write(open('static/standart_img/standart.jpg', 'rb').read())
        db_sess.commit()
        form = LoginForm()
        login_user(user, remember=form.remember_me.data)
        return redirect('/basic')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/profile/<user_id>', methods=['GET', 'Post'])
def profile(user_id):
    db_sess = db_session.create_session()
    try:
        user = db_sess.query(User).get(int(user_id))
    except ValueError:
        return render_template('Error.html', error='Указан неверный или несуществующий id', title='Ошибка!')
    morph = pymorphy3.MorphAnalyzer()
    word1 = morph.parse('задание')[0]
    w = word1.make_agree_with_number(len(user.lst_complete_task.split())).word
    w = f'Вы выполнили {len(user.lst_complete_task.split())} {w}!'
    if request.method == 'GET':
        if user is None:
            return render_template('Error.html', error='Указан неверный или несуществующий id', title='Ошибка!')
        if user != current_user:
            return render_template('Error.html', error='У вас нет прав доступа к профилю пользователя', title='Ошибка!')
        return render_template('profile.html', title=current_user.name,t=w)
    elif request.method == 'POST':
        photo = request.files['photo']
        username = request.form['username']
        password = request.form['password']
        if photo:
            with open(f'static/User_profile_img/user{user_id}.jpg', 'wb') as img:
                img.write(photo.read())
        if username:
            user.name = username
        if password:
            user.check_password = password
        db_sess.commit()
        message = "Данные успешно изменены!"
        return render_template('profile.html', message=message, title=current_user.name,t=w)


@app.route('/top')
def top():
    db_sess = db_session.create_session()
    zxc = []
    for i in db_sess.query(User).all():
        zxc.append([i.name, i.progress, i.photo])
    zxc = sorted(zxc, key=lambda x: (x[1], x[0]))[:100]
    return render_template('top.html', title='Топ пользователей', top=zxc)


@login_required
@app.route('/task/<level_n>/<task_n>', methods=['GET', 'Post'])
def task(level_n, task_n):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(int(current_user.id))
    k = int(level_n.split('_')[-1])
    reward = 0
    if level_n == 'level_1':
        reward = eval(f'l1_{task_n}.main()')
    if level_n == 'level_3':
        reward = eval(f'l3_{task_n}.main()')
    if request.method == 'POST':
        if level_n == 'level_2':
            if task_n == 'task_1':
                res = request.form['level_2_task_1']
                reward = str(l2_task_1.main()) == res
    user.progress += reward * k
    if reward:
        user.lst_complete_task += f' {level_n}:{task_n}'
    db_sess.commit()
    return redirect('/basic')


@app.errorhandler(404)
def pageNot(error):
    return render_template('Error.html', error='Страница не найдена!', title='Ошибка!')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/basic")


if __name__ == '__main__':
    main()
