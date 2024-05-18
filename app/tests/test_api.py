import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Send, Reply

class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('app.config.TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        self.create_user_and_note()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_user_and_note(self):
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('testpassword')
        db.session.add(self.user)
        db.session.commit()

        self.note = Send(body='This is a test message', author=self.user, labels='test', anonymous=False)
        db.session.add(self.note)
        db.session.commit()

    def login(self):
        return self.client.post(url_for('main.login'), json={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)

    def test_random_other_note_no_note(self):
        self.login()
        response = self.client.get(url_for('main.random_other_note'))
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'No other notes available', response.data)

    def test_random_other_note_with_note(self):
        self.login()
        # Create a second user and note
        other_user = User(username='otheruser', email='other@example.com')
        other_user.set_password('otherpassword')
        db.session.add(other_user)
        db.session.commit()

        other_note = Send(body='This is another test message', author=other_user, labels='test', anonymous=True)
        db.session.add(other_note)
        db.session.commit()

        response = self.client.get(url_for('main.random_other_note'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is another test message', response.data)

    def test_random_note_by_label_no_note(self):
        self.login()
        response = self.client.get(url_for('main.random_note_by_label', label='nonexistent'))
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'No notes available with the given label', response.data)

    def test_random_note_by_label_with_note(self):
        self.login()
        response = self.client.get(url_for('main.random_note_by_label', label='test'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is a test message', response.data)

    def test_get_notes_with_replies(self):
        self.login()
        response = self.client.get(url_for('main.api_get_notes_with_replies', username='testuser'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'notes_with_replies', response.data)

    def test_note_reply_detail(self):
        self.login()
        reply = Reply(body='This is a test reply', author=self.user, sendId=self.note.id, anonymous=False)
        db.session.add(reply)
        db.session.commit()

        response = self.client.get(url_for('main.api_note_reply_detail', username='testuser', note_id=self.note.id, reply_id=reply.id))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is a test reply', response.data)

if __name__ == '__main__':
    unittest.main()
