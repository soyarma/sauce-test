# -*- coding: utf-8 -*-
import os
import sys
import base64
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import sauceclient
from sauceclient import SauceClient

USERNAME = os.environ.get('SAUCE_USERNAME', '')
ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY', '')
WEB_IP = os.environ.get('DOCKER_WEB_IP', '');
sauce = SauceClient(USERNAME, ACCESS_KEY)

print ("Sauce is testing IP/URL: %s" % str(WEB_IP))

class MassQuoteFlow(unittest.TestCase):
    def setUp(self):
        desired_cap = {
            'platform': "Windows 10",
            'browserName': "chrome",
            'version': "49",
            'name': "Insuramatch Massachusetts Quote Flow"
        }
        sauce_url = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub"
        base_url = "http://%s"
        self.driver = webdriver.Remote(
            command_executor=sauce_url % (USERNAME, ACCESS_KEY),
            desired_capabilities=desired_cap)
        self.driver.implicitly_wait(10)
        self.base_url = base_url % (WEB_IP)
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_mass_quote_flow(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("edit-zipcode").click()
        driver.find_element_by_id("edit-zipcode").clear()
        driver.find_element_by_id("edit-zipcode").send_keys("01923")
        driver.find_element_by_id("edit-submit--2").click()
#        self.assertEqual("Auto", driver.find_element_by_id("edit-submitted-product-list").get_attribute("value"))
        driver.find_element_by_id("edit-submitted-product-list").click()
        Select(driver.find_element_by_id("edit-submitted-product-list")).select_by_visible_text("Auto")
        driver.find_element_by_css_selector("option[value=\"45\"]").click()
        driver.find_element_by_id("edit-submitted-first-name").click()
        driver.find_element_by_id("edit-submitted-first-name").clear()
        driver.find_element_by_id("edit-submitted-first-name").send_keys("Michael")
        driver.find_element_by_id("edit-submitted-last-name").clear()
        driver.find_element_by_id("edit-submitted-last-name").send_keys("Cooper")
        driver.find_element_by_id("edit-submitted-phone").clear()
        driver.find_element_by_id("edit-submitted-phone").send_keys("9784736139")
        driver.find_element_by_id("edit-submitted-email").click()
        driver.find_element_by_id("edit-submitted-email").clear()
        driver.find_element_by_id("edit-submitted-email").send_keys("soyarma@soyarma.net")
        Select(driver.find_element_by_id("edit-submitted-state")).select_by_visible_text("Massachusetts")
#        self.assertEqual("01923", driver.find_element_by_id("edit-submitted-zip").get_attribute("value"))
        driver.find_element_by_id("edit-submitted-zip").click()
        driver.find_element_by_id("edit-submitted-zip").clear()
        driver.find_element_by_id("edit-submitted-zip").send_keys("01923")
        driver.find_element_by_css_selector("#webform-client-form-1621 > div > button[name=\"op\"]").click()
        self.assertEqual("THANK YOU! YOUR REQUEST HAS BEEN SUCCESSFULLY SUBMITTED!", driver.find_element_by_css_selector("h2.text-center").text)

        
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
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
        print("Link to your job: https://saucelabs.com/jobs/%s" % self.driver.session_id)
        try:
            if sys.exc_info() == (None, None, None):
                sauce.jobs.update_job(self.driver.session_id, passed=True)
            else:
                sauce.jobs.update_job(self.driver.session_id, passed=False)
        finally:
            self.driver.quit()
            self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

