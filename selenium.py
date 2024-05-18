import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class SeleniumTestCase(unittest.TestCase):

    def setUp(self):
        if self.browser == 'chrome':
            self.driver = webdriver.Chrome()
        elif self.browser == 'firefox':
            self.driver = webdriver.Firefox()
        elif self.browser == 'safari':
            self.driver = webdriver.Safari()
        elif self.browser == 'edge':
            self.driver = webdriver.Edge()
        else:
            raise ValueError(f'Unsupported browser: {self.browser}')  

    def tearDown(self):
        self.driver.quit()

    def test_register_and_login(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000/register')

        # register
        username_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        password2_input = driver.find_element(By.NAME, 'password2')
        submit_button = driver.find_element(By.NAME, 'submit')

        username_input.send_keys('newuser')
        password_input.send_keys('newpassword')
        password2_input.send_keys('newpassword')
        submit_button.click()

        # check registration successful
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'Registration successful')
        )

        # logout
        driver.get('http://127.0.0.1:5000/logout')

        # login
        driver.get('http://127.0.0.1:5000/login')
        username_input = driver.find_element(By.NAME, 'username')
        password_input = driver.find_element(By.NAME, 'password')
        submit_button = driver.find_element(By.NAME, 'submit')

        username_input.send_keys('newuser')
        password_input.send_keys('newpassword')
        submit_button.click()

        # check login successful
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'Welcome, newuser')
        )

if __name__ == '__main__':
    unittest.main()
