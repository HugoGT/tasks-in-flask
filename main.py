from unittest import TextTestRunner, TestLoader

from flask import make_response, redirect, render_template, flash, url_for
from flask_login import login_required, current_user

from app import create_app
from app.models import TaskForm, DeleteTaskForm, UpdateTaskForm
from app.firestore_service import put_task, update_task, delete_task, get_tasks


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

    response = make_response(redirect('/welcome'))

    return response


@app.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
    username = current_user.id
    task_form = TaskForm()
    delete_form = DeleteTaskForm()
    update_form = UpdateTaskForm()

    if task_form.validate_on_submit():
        put_task(user_id=username, description=task_form.description.data)

        flash('La tarea se creó con éxito!')

    context = {
        'username': username,
        'task_form': task_form,
        'delete_form': delete_form,
        'update_form': update_form,
        'tasks': get_tasks(user_id=username),
    }

    return render_template('hi.html', **context)


@app.route('/tasks/update/<task_id>/<int:done>', methods=['POST'])
def update(task_id, done):
    user_id = current_user.id

    update_task(user_id, task_id, done)

    return redirect(url_for('welcome'))


@app.route('/tasks/delete/<task_id>', methods=['POST'])
def delete(task_id):
    user_id = current_user.id
    delete_task(user_id, task_id)

    return redirect(url_for('welcome'))