from flask import Flask, render_template, redirect, request
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from create_database import create_database
from users import Users as User
import schedule
from planets import Planets
from news import News
from datetime import datetime, timedelta
from flask_login import LoginManager, login_user
import apod_object_parser
import requests
import os
import time
from translater import translate_text
app = Flask(__name__, template_folder='templates')
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
UPLOAD_FOLDER = 'static/img/avatars'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def news_add_new(response):  # обновление новостей из картинок дня Nasa
    db = create_database(load_fake_data=False)
    # при заполнении базы данных были перепутаны колонки title и author
    if not db.query(News).filter(News.author == response['title']).first():
        des = response['explanation']
        title = response['title']
        date = response['date']
        if 'copyright' in response:
            author = response['copyright']
        else:
            author = None
        planets = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
        db = create_database(load_fake_data=False)
        for i in range(8):
            if planets[i] in title.lower():
                planet_id = i + 1
                des = translate_text(des)
                title = translate_text(title)
                new = News(author, title, des, f'{date}.jpg', planet_id)
                db.add(new)
        db.commit()


# проверка на то, что файл аватарки правильного формата
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
            planet_id=1,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.add(user)
        db.commit()
        user = db.query(User).filter(User.email == form.email.data).first()
        id = user.id
        return redirect(f'/test/{id}')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/users_page/<id>', methods=['GET', 'POST'])
def users_page(id):
    id = int(id)
    if request.method == 'POST':  # смена аватарки у пользователя
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{id}.png'))
    # загрузка новостей для планеты пользователя
    db = create_database(load_fake_data=False)
    user = db.query(User).get(id)
    planet_id = user.planet_id
    planet = db.query(Planets).get(planet_id)
    planet_news = db.query(News).filter(News.planet_id == planet_id)
    pl_news = []
    dates = []
    # проверка, чтобы не было повторяющихся новостей в ленте
    for i in planet_news:
        if i.url_source not in dates:
            pl_news.append(i)
            dates.append(i.url_source)
    # сортировка новостей по дате, чтобы свежие новости были в топе
    pl_news = sorted(pl_news, key=lambda x: x.url_source, reverse=True)
    planet_img = planet.planet_image
    planet_name = planet.planet_name
    # проверка на наличие аватарки у пользователя
    if os.path.exists(f'static/img/avatars/{id}.png'):
        return render_template('users_page.html', id=id, avatar=f'{id}.png',
                               planet=planet_img, news=pl_news,
                               planet_name=planet_name)
    # если её нет, то на аватарке стоит дефолтная картинка
    return render_template('users_page.html', id=id, avatar='ava.png',
                           planet=planet_img, news=pl_news,
                           planet_name=planet_name)


@app.route('/organize_a_mission/<ids>', methods=['POST', 'GET'])
def organize_a_mission(ids):
    ids = int(ids)
    # организация перелётов
    if request.method == 'POST':
        if 'submit' in request.form:
            form = request.form
            db_sess = create_database(load_fake_data=False)
            user_id = ids
            planet_id = form.get('planet_id')
            planet_id = int(planet_id)
            user = db_sess.query(User).get(user_id)
            user.planet_id = planet_id
            user.end_date = datetime.now() + timedelta(hours=3)  # недоделанная функция таймера на полёт
            db_sess.commit()
            return redirect(f"/users_page/{user_id}")
    return render_template('create_mission.html', id=ids)


@app.route('/not_now')
def not_now():
    # страница в разработке
    return render_template('no_page.html')


@app.route('/test/<id>', methods=['GET', 'POST'])
def test(id):
    if request.method == 'POST':
        if 'submit' in request.form:
            # прохождение теста и присуждение планеты пользователю
            planet_id = request.form.get('planet_id')
            db = create_database(load_fake_data=False)
            user = db.query(User).get(int(id))
            user.planet_id = planet_id
            db.commit()
            return redirect(f'/users_page/{id}')
    return render_template('test.html')


@app.route('/quiz')
def quiz():
    return render_template('викторина.html')


def get_data_from_nasa_api():
    api_key = 'DEMO_KEY'
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    response = requests.get(url).json()
    if 'hdurl' in response:
        url = response['hdurl']
        date = str(datetime.now()).split()[0]
        apod_object_parser.download_image(url, date)  # загрузка картинки новости по ссылке
        news_add_new(response)


schedule.every(24).hours.do(get_data_from_nasa_api)  # ограничение на запросы к NASA API каждый день


# Функция для запуска проверки расписания
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


import threading  # импорт здесь специально, чтобы таймер на обновление новостей и сам сайт работали одновременно
thread = threading.Thread(target=run_schedule)
thread.start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
