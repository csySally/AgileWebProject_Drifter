import unittest
from app import create_app, db
from app.models import User
from app.forms import LoginForm, RegistrationForm, SendForm, ReplyForm

class FormsTestCase(unittest.TestCase):

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

    def test_login_form_valid_data(self):
        # Test login form with valid data
        form = LoginForm(username='testuser', password='testpassword')
        self.assertTrue(form.validate())

    def test_login_form_missing_username(self):
    # Test login form with missing username
        form = LoginForm(username='', password='testpassword')
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.username.errors)

    def test_login_form_missing_password(self):
        # Test login form with missing password
        form = LoginForm(username='testuser', password='')
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.password.errors)

    def test_registration_form_valid_data(self):
        # Test registration form with valid data
        form = RegistrationForm(username='newuser', password='newpassword', password2='newpassword')
        self.assertTrue(form.validate())

    def test_registration_form_mismatched_passwords(self):
        # Test registration form with mismatched passwords
        form = RegistrationForm(username='newuser', password='newpassword', password2='wrongpassword')
        self.assertFalse(form.validate())
        self.assertIn('Field must be equal to password.', form.password2.errors)

    def test_registration_form_duplicate_username(self):
        # Test registration form with duplicate username
        user = User(username='existinguser')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        form = RegistrationForm(username='existinguser', password='newpassword', password2='newpassword')
        self.assertFalse(form.validate())
        self.assertIn('Please use a different username.', form.username.errors)

    def test_send_form_valid_data(self):
        # Test send form with valid data
        form = SendForm(send='This is a test message', label='testlabel', anonymous=False)
        self.assertTrue(form.validate())

    def test_send_form_missing_send(self):
        # Test send form with missing send
        form = SendForm(send='', label='testlabel', anonymous=False)
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.send.errors)

    def test_reply_form_valid_data(self):
        # Test reply form with valid data
        form = ReplyForm(reply='This is a test reply', send_id='1', anonymous=False)
        self.assertTrue(form.validate())

    def test_reply_form_missing_reply(self):
        # Test reply form with missing reply
        form = ReplyForm(reply='', send_id='1', anonymous=False)
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.reply.errors)

if __name__ == '__main__':
    unittest.main()
