import firebase_admin
from firebase_admin import credentials, firestore

credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()


def get_users():
    return db.collection('users').get()


def get_user(user_id):
    return db.collection('users').document(user_id).get()


def user_put(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({'password': user_data.password})


def get_tasks(user_id):
    return db.collection('users').document(user_id).collection('tasks').get()


def put_task(user_id, description):
    task_collection_ref = db.collection('users').document(user_id).collection('tasks')
    task_collection_ref.add({'description': description, 'done': False})


def update_task(user_id, task_id, done):
    task_done = not bool(done)
    task_ref = _get_task_ref(user_id, task_id)
    task_ref.update({'done': task_done})


def delete_task(user_id, task_id):
    task_ref = _get_task_ref(user_id, task_id)
    task_ref.delete()


def _get_task_ref(user_id, task_id):
    return db.document(f'users/{user_id}/tasks/{task_id}')