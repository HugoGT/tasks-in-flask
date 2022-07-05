from unittest import TextTestRunner, TestLoader

from flask import request, make_response, redirect, render_template, session
from flask_login import login_required, current_user

from app import create_app
from app.firestore_service import get_users, get_tasks


to_do_list = ['Hacer curso de Flask', 'Hacer la compra', 'Hacer examen de carrera']

app = create_app()


@app.cli.command()
def test():
    tests = TestLoader().discover('tests')
    TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/welcome'))
    session['user_ip'] = user_ip

    return response


@app.route('/welcome', methods=['GET'])
@login_required
def welcome():
    user_ip = session.get('user_ip')
    username = current_user.id

    context = {
        'user_ip': user_ip,
        'to_do_list': get_tasks(user_id=username),
        'username': username,
    }

    return render_template('hi.html', **context)