from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/login')
def login():
    return render_template('login.html', title='')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)