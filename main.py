from flask import Flask, request, make_response, redirect, render_template


app = Flask(__name__)

to_do_list = ['Hacer curso de Flask', 'Hacer la compra', 'Hacer examen de carrera']


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