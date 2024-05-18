import unittest
import multiprocessing
import time
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
from selenium.webdriver.chrome.options import Options
from app import create_app, db
from app.config import TestingConfig

localHost = "http://127.0.0.1:5000/"

def run_flask_app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5000)

class SeleniumTestCase(unittest.TestCase):

    def setUp(self):
        self.testApp = create_app(TestingConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        
        self.server_process = multiprocessing.Process(target=run_flask_app)
        self.server_process.start()
        time.sleep(3)  

        options = Options()
        # options.add_argument("--headless")  
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(localHost)

    def tearDown(self):
        self.driver.quit()

        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        self.server_process.terminate()
        self.server_process.join() 

    def test_register_and_login(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000/register')

        unique_username = f"user{uuid.uuid4().hex[:6]}"
        password = "Password1"

        try:
            username_input = driver.find_element(By.NAME, 'username')
            password_input = driver.find_element(By.NAME, 'password')
            password2_input = driver.find_element(By.NAME, 'confirmPassword')
            submit_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-sign-in')

            username_input.send_keys(unique_username)
            password_input.send_keys(password)
            password2_input.send_keys(password)
            submit_button.click()

            try:
                alert = driver.switch_to.alert
                alert_text = alert.text
                print(f"Alert text: {alert_text}")
                self.assertEqual(alert_text, 'You have registered successfully!')
                alert.accept()
                print("Registration successful.")
            except NoAlertPresentException:
                print("No alert present after registration.")

            driver.get('http://127.0.0.1:5000/logout')

            driver.get('http://127.0.0.1:5000/login')
            username_input = driver.find_element(By.NAME, 'username')
            password_input = driver.find_element(By.NAME, 'password')
            submit_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-sign-in')

            username_input.send_keys(unique_username)
            password_input.send_keys(password)
            submit_button.click()

            time.sleep(5) 
            current_url = driver.current_url

            self.assertIn('/user/', current_url)
            body_text = driver.find_element(By.TAG_NAME, 'body').text
            self.assertIn(unique_username, body_text)
            print(f"Username {unique_username} found on user page.")

        except NoSuchElementException as e:
            print(f"Element not found: {e}")
            self.fail("Test failed due to missing element.")

if __name__ == '__main__':
    unittest.main()
