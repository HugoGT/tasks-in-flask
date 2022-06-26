from flask import Flask, request, make_response, redirect, render_template
from flask_bootstrap import Bootstrap

to_do_list = ['Hacer curso de Flask', 'Hacer la compra', 'Hacer examen de carrera']


app = Flask(__name__, template_folder='./templates', static_folder='./static')
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'Clave secreta'


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
    response.set_cookie('user_ip', user_ip)

    return response


@app.route('/welcome')
def greeting():
    user_ip = request.cookies.get('user_ip')
    context = {
        'user_ip': user_ip,
        'to_do_list': to_do_list,
    }

    return render_template('hi.html', **context)