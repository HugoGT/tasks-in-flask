from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from forms import LoginForm


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
    session['user_ip'] = user_ip

    return response


@app.route('/welcome', methods=['GET', 'POST'])
def greeting():
    user_ip = session.get('user_ip')
    username = session.get('username')
    login_form = LoginForm()

    context = {
        'user_ip': user_ip,
        'to_do_list': to_do_list,
        'login_form': login_form,
        'username': username,
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username

        flash('Nombre de usuario registrado correctamente!')

        return redirect(url_for('index'))

    return render_template('hi.html', **context)