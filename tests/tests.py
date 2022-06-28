from flask import current_app, url_for
from flask_testing import TestCase

from main import app


class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        return app

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_index_redirects(self):
        response = self.client.get(url_for('index'))

        self.assertRedirects(response, url_for('welcome'))

    def test_welcome_get(self):
        response= self.client.get(url_for('welcome'))

        self.assert200(response)

    def test_welcome_post(self):
        fake_form = {
            'username': 'fake-username',
            'password': 'fake-password',
        }
        response = self.client.post(url_for('welcome'), data=fake_form)

        self.assertRedirects(response, url_for('index'))