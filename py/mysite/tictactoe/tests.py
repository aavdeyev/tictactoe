from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase

class DrawTest1(LiveServerTestCase):
    
    fixtures = ['admin.json']

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_draw(self):
        driver = self.driver
        driver.get(self.base_url + "/accounts/login/")
        username_field = driver.find_element_by_name("username")
        username_field.clear()
        username_field.send_keys("mama")
        password_field = driver.find_element_by_name("password")
        password_field.clear()
        password_field.send_keys("veta")
        driver.find_element_by_name("login").click()
        driver.find_element_by_id("sqr3").click()
        driver.find_element_by_id("sqr9").click()
        driver.find_element_by_id("sqr4").click()
        driver.find_element_by_id("sqr8").click()
        self.assertEqual("Draw", self.close_alert_and_get_its_text())
        self.accept_next_alert = False
        driver.find_element_by_id("logout_ref").click()
        self.assertRegexpMatches(self.close_alert_and_get_its_text(), r"^Save current game[\s\S]$")
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

class Lose(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_lose(self):
        driver = self.driver
        driver.get(self.base_url + "/accounts/login/")
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("mama")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("veta")
        driver.find_element_by_name("login").click()
        driver.find_element_by_id("sqr6").click()
        self.assertEqual("You just made a fatal mistake and will lose this game.You should never hit a side button in step 1", self.close_alert_and_get_its_text())
        driver.find_element_by_id("sqr8").click()
        self.assertEqual("You Lose!", self.close_alert_and_get_its_text())
        self.accept_next_alert = False
        driver.find_element_by_id("logout_ref").click()
        self.assertRegexpMatches(self.close_alert_and_get_its_text(), r"^Save current game[\s\S]$")
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
