import flask
from flask import jsonify, Flask, make_response, request

from create_database import create_database
from users import Users
from planets import Planets

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db = create_database(load_fake_data=False)
    jobs = db.query(Users).all()
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'jobs':
                [item.to_dict()
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<job_id>', methods=['GET'])
def get_job(job_id):
    if not job_id.isdigit():
        return make_response(jsonify({'error': 'Bad Request'}), 400)
    job_id = int(job_id)
    db = create_database(load_fake_data=False)
    jobs = db.query(Jobs).get(job_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'jobs':
                [jobs.to_dict()]
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db = create_database(load_fake_data=False)
    jobs = Jobs(request.json['team_leader'], request.json['job'], request.json['work_size'],
                request.json['collaborators'], request.json['is_finished'])
    db.add(jobs)
    db.commit()
    return jsonify({'id': jobs.id})


@blueprint.route('/api/jobs/<job_id>', methods=['DELETE'])
def delete_news(job_id):
    if not job_id.isdigit():
        return make_response(jsonify({'error': 'Bad request'}), 400)
    job_id = int(job_id)
    db = create_database(load_fake_data=False)
    jobs = db.query(Jobs).get(job_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db.delete(jobs)
    db.commit()
    return jsonify({'success': 'OK'})


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)