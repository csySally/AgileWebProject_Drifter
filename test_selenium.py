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
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

localHost = "http://127.0.0.1:5000/"

def run_flask_app():
    # Create a Flask app using the testing configuration
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5000)

class SeleniumTestCase(unittest.TestCase):

    def setUp(self):
        # Setup method to initialize the test environment
        self.testApp = create_app(TestingConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        
        # Start the Flask app in a separate process for testing
        self.server_process = multiprocessing.Process(target=run_flask_app)
        self.server_process.start()
        time.sleep(3)  

        options = Options()
        # options.add_argument("--headless")  
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(localHost)

    def tearDown(self):
        # Teardown method to clean up after tests
        self.driver.quit()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        self.server_process.terminate()
        self.server_process.join() 

    def test_register_and_login(self):
        # Test case for registering and logging in a user
        driver = self.driver
        driver.get('http://127.0.0.1:5000/register')

        self.unique_username = f"user{uuid.uuid4().hex[:6]}" # Generate a unique username
        password = "Password1"

        try:
            # Find the registration form inputs and submit button
            username_input = driver.find_element(By.NAME, 'username')
            password_input = driver.find_element(By.NAME, 'password')
            password2_input = driver.find_element(By.NAME, 'confirmPassword')
            submit_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-sign-in')
            # Fill in the registration form and submit it
            username_input.send_keys(self.unique_username)
            password_input.send_keys(password)
            password2_input.send_keys(password)
            submit_button.click()

            try:
                # Check for a successful registration alert
                alert = driver.switch_to.alert
                alert_text = alert.text
                print(f"Alert text: {alert_text}")
                self.assertEqual(alert_text, 'You have registered successfully!')
                alert.accept()
                print("Registration successful.")
            except NoAlertPresentException:
                print("No alert present after registration.")

            #driver.get('http://127.0.0.1:5000/logout')

            driver.get('http://127.0.0.1:5000/login')
            # Find the login form inputs and submit button
            username_input = driver.find_element(By.NAME, 'username')
            password_input = driver.find_element(By.NAME, 'password')
            submit_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-sign-in')
            # Fill in the login form and submit it
            username_input.send_keys(self.unique_username)
            password_input.send_keys(password)
            submit_button.click()

            time.sleep(5) 
            current_url = driver.current_url
            # Check if the user is redirected to their user page
            self.assertIn('/user/', current_url)
            body_text = driver.find_element(By.TAG_NAME, 'body').text
            self.assertIn(self.unique_username, body_text)
            print(f"Username {self.unique_username} found on user page.")

        except NoSuchElementException as e:
            # Handle the case where an element is not found
            print(f"Element not found: {e}")
            self.fail("Test failed due to missing element.")
            
            
            
    def test_send_message(self):
        # First, register and log in to the application
        self.test_register_and_login() 

        driver = self.driver
         # Navigate to the user's page
        driver.get(localHost + 'user/' + self.unique_username)

        try:
             # Find and click the draft link to start composing a new message
            draft_link = driver.find_element(By.ID, 'draft')
            draft_link.click()
            time.sleep(2) 
            # Enter the message text into the note input field
            note_input = driver.find_element(By.ID, 'noteInput')
            next_button = driver.find_element(By.ID, 'btn-next')
            note_input.send_keys("This is a test message.")
            next_button.click()
            time.sleep(2) 
            # Enter a label for the message and submit it
            label_input = driver.find_element(By.ID, 'labelInput')
            label_input.send_keys("test")
            label_input.send_keys(Keys.RETURN)
            time.sleep(1)  
             # Find and click the OK button to finalize sending the message
            ok_button = driver.find_element(By.ID, 'btn-next2')
            ok_button.click()
            time.sleep(2)  
            try:
                # Attempt to switch to the alert if it is present
                WebDriverWait(driver, 10).until(EC.alert_is_present(),
                                     "Waiting for alert to appear after sending note.")
                alert = driver.switch_to.alert
                alert_text = alert.text
                print(f"Alert text: {alert_text}")
                # Assert that the alert text matches the expected message
                self.assertEqual(alert_text, 'You have successfully added a note!')
                alert.accept()
            except NoAlertPresentException:
                print("No alert present after sending note.")

            time.sleep(2)  
            # Retrieve the current URL of the web page
            current_url = driver.current_url
            # Assert that the current URL contains the unique username path, indicating successful navigation
            self.assertIn('/user/' + self.unique_username, current_url)
            print("Returned to user page.")

        except NoSuchElementException as e:
            print(f"Element not found: {e}")
            self.fail("Test failed due to missing element.")


if __name__ == '__main__':
    unittest.main()
