import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Send, Reply
from werkzeug.security import generate_password_hash

class RoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('app.config.TestingConfig')
        self.app.config['SERVER_NAME'] = 'localhost.localdomain'  
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        self.create_user()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_user(self):
        user = User(username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

    def login(self, username, password):
        # Log in with the given username and password
        return self.client.post(url_for('main.login'), json={
            'username': username,
            'password': password
        }, follow_redirects=True)

    def logout(self):
        # Log out the current user
        return self.client.post(url_for('main.logout'), follow_redirects=True)

    def test_login_page(self):
        # Test the login page
        response = self.client.get(url_for('main.login'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_valid_login(self):
        # Test logging in with valid credentials
        response = self.login('testuser', 'testpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)

    def test_invalid_login(self):
        # Test logging in with invalid credentials
        response = self.login('wronguser', 'wrongpassword')
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid username or password', response.data)

    def test_logout(self):
        # Test logging out
        self.login('testuser', 'testpassword')
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_register(self):
        # Test user registration
        response = self.client.post(url_for('main.register'), json={
            'username': 'newuser',
            'password': 'newpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)

    def test_index_redirect(self):
        # Test redirect to login page
        response = self.client.get(url_for('main.index'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(url_for('main.login', _external=False), response.location)

    def test_user_page(self):
        # Test user page
        self.login('testuser', 'testpassword')
        response = self.client.get(url_for('main.user', username='testuser'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testuser', response.data)

    def test_get_user_info(self):
        # Test getting user information
        self.login('testuser', 'testpassword')
        response = self.client.get(url_for('main.get_user_info'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testuser', response.data)

    def test_send_note(self):
        # Test sending a note
        self.login('testuser', 'testpassword')
        response = self.client.post(url_for('main.send', username='testuser'), json={
            'note': 'This is a test note',
            'anonymous': False,
            'labels': 'test'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your message has been sent!', response.data)

    def test_random_other_note(self):
        # Test getting a random note from another user
        self.login('testuser', 'testpassword')
        response = self.client.get(url_for('api.random_other_note'))
        self.assertEqual(response.status_code, 404)  # Assuming no other notes exist

    def test_random_note_by_label(self):
        # Test getting a random note by label
        self.login('testuser', 'testpassword')
        response = self.client.get(url_for('api.random_note_by_label', label='test'))
        self.assertEqual(response.status_code, 404)  # Assuming no notes with label exist

    def test_reply_note(self):
        # Test replying to a note
        self.login('testuser', 'testpassword')
        response = self.client.get(url_for('main.reply_note'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reply', response.data)

    def test_check_my_reply(self):
        # Test checking replies to notes
        self.login('testuser', 'testpassword')
        response = self.client.get(url_for('main.check_my_reply'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Check', response.data)

    def test_api_get_notes_with_replies(self):
        # Test getting notes with replies
        self.login('testuser', 'testpassword')
        response = self.client.get(url_for('api.get_notes_with_replies', username='testuser'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'notes_with_replies', response.data)


    def test_upload_image(self):
        # Test uploading an image
        self.login('testuser', 'testpassword')
        with open('tests/test_image.jpg', 'rb') as img:
            response = self.client.post(url_for('main.upload_image'), content_type='multipart/form-data', data={
                'image': img
            }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Image uploaded successfully', response.data)

if __name__ == '__main__':
    unittest.main()
