import unittest
from app import create_app, db
from app.models import User, Send, Reply

class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('app.config.TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        user = User(username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(user.id)
        self.assertTrue(user.check_password('testpassword'))
        self.assertEqual(user.username, 'testuser')

    def test_send_creation(self):
        user = User(username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        send = Send(body='This is a test message', author=user, labels='test', anonymous=False)
        db.session.add(send)
        db.session.commit()
        self.assertIsNotNone(send.id)
        self.assertEqual(send.body, 'This is a test message')
        self.assertEqual(send.author.username, 'testuser')

    def test_reply_creation(self):
        user = User(username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        send = Send(body='This is a test message', author=user, labels='test', anonymous=False)
        db.session.add(send)
        db.session.commit()

        reply = Reply(body='This is a test reply', author=user, sendId=send.id, anonymous=False)
        db.session.add(reply)
        db.session.commit()
        self.assertIsNotNone(reply.id)
        self.assertEqual(reply.body, 'This is a test reply')
        self.assertEqual(reply.author.username, 'testuser')
        self.assertEqual(reply.sendId, send.id)

    def test_user_to_dict(self):
        user = User(username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
        user_dict = user.to_dict()
        self.assertEqual(user_dict['username'], 'testuser')

    def test_send_to_dict(self):
        user = User(username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        send = Send(body='This is a test message', author=user, labels='test', anonymous=False)
        db.session.add(send)
        db.session.commit()
        send_dict = send.to_dict()
        self.assertEqual(send_dict['body'], 'This is a test message')

    def test_reply_to_dict(self):
        user = User(username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        send = Send(body='This is a test message', author=user, labels='test', anonymous=False)
        db.session.add(send)
        db.session.commit()

        reply = Reply(body='This is a test reply', author=user, sendId=send.id, anonymous=False)
        db.session.add(reply)
        db.session.commit()
        reply_dict = reply.to_dict()
        self.assertEqual(reply_dict['body'], 'This is a test reply')

if __name__ == '__main__':
    unittest.main()
