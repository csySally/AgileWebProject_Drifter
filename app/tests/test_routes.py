import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Send, Reply
from werkzeug.security import generate_password_hash

class RoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('app.config.TestingConfig')
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
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

    def login(self, username, password):
        return self.client.post(url_for('main.login'), json={
            'username': username,
            'password': password
        }, follow_redirects=True)

    def logout(self):
        return self.client.post(url_for('main.logout'), follow_redirects=True)

    def test_login_page(self):
        response = self.client.get(url_for('main.login'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_valid_login(self):
        response = self.login('testuser', 'testpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)

    def test_invalid_login(self):
        response = self.login('wronguser', 'wrongpassword')
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid username or password', response.data)

    def test_logout(self):
        self.login('testuser', 'testpassword')
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_register(self):
        response = self.client.post(url_for('main.register'), json={
            'username': 'newuser',
            'password': 'newpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)

    def test_index_redirect(self):
        response = self.client.get(url_for('main.index'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(url_for('main.login'), response.location)

    def test_user_page(self):
        self.login('testuser', 'testpassword')
        response = self.client.get(url_for('main.user', username='testuser'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testuser', response.data)

    def test_get_user_info(self):
        self.login('testuser', 'testpassword')
        response = self.client.get(url_for('main.get_user_info'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testuser', response.data)

    def test_send_note(self):
        self.login('testuser', 'testpassword')
        response = self.client.post(url_for('main.send', username='testuser'), json={
            'note': 'This is a test note',
            'anonymous': False,
            'labels': 'test'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your message has been sent!', response.data)

    def test_random_other_note(self):
        self.login('testuser', 'testpassword')
        response = self.client.get(url_for('main.random_other_note'))
        self.assertEqual(response.status_code, 404)  # Assuming no other notes exist

    def test_random_note_by_label(self):
        self.login('testuser', 'testpassword')
        response = self.client.get(url_for('main.random_note_by_label', label='test'))
        self.assertEqual(response.status_code, 404)  # Assuming no notes with label exist

    def test_reply_note(self):
        self.login('testuser', 'testpassword')
        response = self.client.get(url_for('main.reply_note'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reply', response.data)

    def test_check_my_reply(self):
        self.login('testuser', 'testpassword')
        response = self.client.get(url_for('main.check_my_reply'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Check', response.data)

    def test_api_get_notes_with_replies(self):
        self.login('testuser', 'testpassword')
        response = self.client.get(url_for('main.api_get_notes_with_replies', username='testuser'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'notes_with_replies', response.data)

    def test_reply_to_note(self):
        self.login('testuser', 'testpassword')
        # First, send a note to reply to
        self.client.post(url_for('main.send', username='testuser'), json={
            'note': 'This is a test note',
            'anonymous': False,
            'labels': 'test'
        })
        note = Send.query.first()
        response = self.client.post(url_for('main.reply', username='testuser'), json={
            'note_id': note.id,
            'reply_body': 'This is a test reply',
            'anonymous': False
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reply successfully posted', response.data)

    def test_sent_notes(self):
        self.login('testuser', 'testpassword')
        response = self.client.get(url_for('main.sent_notes', username='testuser'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'notes_with_replies', response.data)

    def test_api_note_reply_detail(self):
        self.login('testuser', 'testpassword')
        # First, send a note to reply to
        self.client.post(url_for('main.send', username='testuser'), json={
            'note': 'This is a test note',
            'anonymous': False,
            'labels': 'test'
        })
        note = Send.query.first()
        # Then, reply to the note
        self.client.post(url_for('main.reply', username='testuser'), json={
            'note_id': note.id,
            'reply_body': 'This is a test reply',
            'anonymous': False
        })
        reply = Reply.query.first()
        response = self.client.get(url_for('main.api_note_reply_detail', username='testuser', note_id=note.id, reply_id=reply.id))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'note', response.data)
        self.assertIn(b'reply', response.data)

    def test_note_reply_detail(self):
        self.login('testuser', 'testpassword')
        # First, send a note to reply to
        self.client.post(url_for('main.send', username='testuser'), json={
            'note': 'This is a test note',
            'anonymous': False,
            'labels': 'test'
        })
        note = Send.query.first()
        # Then, reply to the note
        self.client.post(url_for('main.reply', username='testuser'), json={
            'note_id': note.id,
            'reply_body': 'This is a test reply',
            'anonymous': False
        })
        reply = Reply.query.first()
        response = self.client.get(url_for('main.note_reply_detail', username='testuser', note_id=note.id, reply_id=reply.id))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'note', response.data)
        self.assertIn(b'reply', response.data)

    def test_upload_image(self):
        self.login('testuser', 'testpassword')
        with open('tests/test_image.png', 'rb') as img:
            response = self.client.post(url_for('main.upload_image'), content_type='multipart/form-data', data={
                'image': img
            }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Image uploaded successfully', response.data)

if __name__ == '__main__':
    unittest.main()
