import unittest
from framework.logger import Logger
from config.desired_caps import desired_caps, uri
from framework.driver import driver
from objects.new_regist import regist_element, regist_msg_data, regist_toast_msg
import time
from appium import webdriver
from framework.base import Base

logger = Logger('New regist').get_logger()
driver = Base(webdriver.Remote(uri, desired_caps))

@unittest.skip('')
class NewRegist(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = driver
        cls.driver.launch_app()
        time.sleep(3)

    def test_regist_btn(self):
        self.driver.find_element(regist_element['regist_btn']).click()
        a = self.driver.find_element(regist_element['search_school'])
        self.assertTrue(a)

    def test_search_school(self):
        self.driver.find_element(regist_element['regist_btn']).click()
        self.driver.find_element(regist_element['search_school']).send_keys("清华大学")
        name = self.driver.find_element(regist_element['name']).text
        self.assertEqual('清华大学', name)