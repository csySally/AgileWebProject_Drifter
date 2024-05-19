import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Send, Reply

class APITestCase(unittest.TestCase):

    def setUp(self):
        # Create a test client and set up the database
        self.app = create_app('app.config.TestingConfig')
        self.app.config['SERVER_NAME'] = 'localhost.localdomain'
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        self.create_user()
    
    def tearDown(self):
        # Clean up the database session and drop all tables
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_user(self):
        # Create a test user
        self.user = User(username='testuser')
        self.user.set_password('testpassword')
        db.session.add(self.user)
        db.session.commit()

    def login(self):
        # Log in the test user
        return self.client.post(url_for('main.login'), json={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)

    def test_random_other_note_no_note(self):
        self.login()
        # Ensure there are no other notes
        Send.query.delete()
        db.session.commit()
        response = self.client.get(url_for('api.random_other_note'))
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'No other notes available', response.data)

    def test_random_other_note_with_note(self):
        self.login()
        # Create a second user and note
        other_user = User(username='otheruser')
        other_user.set_password('otherpassword')
        db.session.add(other_user)
        db.session.commit()

        other_note = Send(body='This is another test message', author=other_user, labels='test', anonymous=True)
        db.session.add(other_note)
        db.session.commit()

        response = self.client.get(url_for('api.random_other_note'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is another test message', response.data)

    def test_random_note_by_label_no_note(self):
        # Ensure there are no notes with the label 'nonexistent'
        self.login()
        response = self.client.get(url_for('api.random_note_by_label', label='nonexistent'))
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'No notes available with the given label', response.data)

    def test_random_note_by_label_with_note(self):
        self.login()
        # Create a second user and note with the label 'test'
        other_user = User(username='otheruser')
        other_user.set_password('otherpassword')
        db.session.add(other_user)
        db.session.commit()

        other_note = Send(body='This is another test message', author=other_user, labels='test', anonymous=True)
        db.session.add(other_note)
        db.session.commit()

        response = self.client.get(url_for('api.random_note_by_label', label='test'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is another test message', response.data)

    def test_get_notes_with_replies(self):
        # Ensure the API endpoint returns notes with replies
        self.login()
        response = self.client.get(url_for('api.get_notes_with_replies', username='testuser'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'notes_with_replies', response.data)

    def test_note_reply_detail(self):
        self.login()
        # Ensure there is a note to reply to
        self.client.post(url_for('main.send', username='testuser'), json={
            'note': 'This is a test message',
            'anonymous': False,
            'labels': 'test'
        }, follow_redirects=True)
        note = db.session.query(Send).first()

        reply = Reply(body='This is a test reply', author=self.user, sendId=note.id, anonymous=False)
        db.session.add(reply)
        db.session.commit()

        response = self.client.get(url_for('api.note_reply_detail', username='testuser', note_id=note.id, reply_id=reply.id))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is a test reply', response.data)

if __name__ == '__main__':
    unittest.main()
