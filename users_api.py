import flask
from flask import jsonify, Flask, make_response, request

from create_database import create_database
from users import Users

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)

db = create_database()
@blueprint.route('/api/users', methods=['GET'])
def get_jobs():
    db = create_database(load_fake_data=False)
    users = db.query(Users).all()
    if not users:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'users':
                [item.to_dict()
                 for item in users]
        }
    )


@blueprint.route('/api/users/<users_id>', methods=['GET'])
def get_job(users_id):
    if not users_id.isdigit():
        return make_response(jsonify({'error': 'Bad Request'}), 400)
    users_id = int(users_id)
    db = create_database(load_fake_data=False)
    users = db.query(Users).get(users_id)
    if not users:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'users':
                [users.to_dict()]
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db = create_database(load_fake_data=False)
    users = Users(request.json['surname'], request.json['name'], request.json['age'],
                request.json['position'], request.json['speciality'], request.json['address'], request.json['email'])
    db.add(users)
    db.commit()
    return jsonify({'id': users.id})


@blueprint.route('/api/users/<users_id>', methods=['DELETE'])
def delete_news(users_id):
    if not users_id.isdigit():
        return make_response(jsonify({'error': 'Bad request'}), 400)
    users_id = int(users_id)
    db = create_database(load_fake_data=False)
    users = db.query(Users).get(users_id)
    if not users:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db.delete(users)
    db.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<users_id>', methods=['PUT'])
def change_job(users_id):
    if not users_id.isdigit():
        return make_response(jsonify({'error': 'Bad request'}), 400)
    users_id = int(users_id)
    db = create_database(load_fake_data=False)
    users = db.query(Users).get(users_id)
    if not users:
        return make_response(jsonify({'error': 'Not found'}), 404)
    keys = ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email']
    for key in request.json:
        if key in keys:
            if key == 'surname':
                users.surname = request.json[key]
            elif key == 'name':
                users.name = request.json[key]
            elif key == 'age':
                users.age = request.json[key]
            elif key == 'position':
                users.position = request.json[key]
            elif key == 'speciality':
                users.speciality = request.json[key]
            elif key == 'address':
                users.address = request.json[key]
            elif key == 'email':
                users.email = request.json[key]
    db.commit()
    return jsonify({'success update id': users.id})


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)