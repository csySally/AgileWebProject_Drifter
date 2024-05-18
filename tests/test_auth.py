import unittest
from flask import url_for
from app import create_app, db
from app.models import User

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test client and set up the database
        self.app = create_app('app.config.TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        # Clean up the database session and drop all tables
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register(self):
        # Test user registration
        response = self.client.post(url_for('main.register'), json={
            'username': 'newuser',
            'password': 'newpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('newpassword'))

    def test_registration_existing_username(self):
        # Test registration with an existing username
        user = User(username='existinguser')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        response = self.client.post(url_for('main.register'), json={
            'username': 'existinguser',
            'password': 'newpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 409)
        self.assertIn(b'Username already exists', response.data)

    def test_valid_login(self):
        # Test logging in with valid credentials
        user = User(username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        response = self.client.post(url_for('main.login'), json={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)

    def test_invalid_login(self):
        # Test logging in with invalid credentials
        response = self.client.post(url_for('main.login'), json={
            'username': 'nonexistentuser',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid username or password', response.data)

    def test_logout(self):
        #   Test logging out
        user = User(username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        self.client.post(url_for('main.login'), json={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)
        response = self.client.post(url_for('main.logout'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_get_user_info(self):
        # Test getting user information
        user = User(username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        self.client.post(url_for('main.login'), json={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)
        response = self.client.get(url_for('main.get_user_info'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testuser', response.data)

if __name__ == '__main__':
    unittest.main()
