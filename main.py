from flask import Flask, render_template, redirect
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from create_database import create_database
from users import Users as User
from flask_login import LoginManager, login_user
app = Flask(__name__, template_folder='templates')
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db = create_database(load_fake_data=False)
    return db.query(User).get(user_id)


@app.route('/')
def root():
    return render_template("main_window.html", title="Главная")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_database(load_fake_data=False)
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            id = user.id
            return redirect(f"/users_page/{id}")
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
        db = create_database(load_fake_data=False)
        if db.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            password=form.password.data,
            planet_id=0,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.add(user)
        db.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/users_page/<id>')
def users_page(id):
    return render_template('users_page.html', id=id, avatar='ava.png', planet='mercury.jfif')


@app.route('/organize_a_mission/<ids>')
def organize_a_mission(ids):
    return render_template('create_mission.html', id=ids)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)