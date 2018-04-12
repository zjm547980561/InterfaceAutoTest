# -*- coding:utf-8 -*-

from framework.logger import Logger
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = Logger('Base').get_logger()


class Base(object):
    def __init__(self, driver):
        self.driver = driver

    def quit(self):
        self.driver.quit()

    def get_window_size_width(self):
        return self.driver.get_window_size()['width']

    def get_window_size_height(self):
        return self.driver.get_window_size()['height']

    def swipe_left(self, num):
        width = self.get_window_size_width()
        height = self.get_window_size_height()

        for i in range(num):
            self.driver.swipe(width * 0.75, height * 0.5, width * 0.25, height * 0.5, 7000)

    def swipe_right(self, num):
        width = self.get_window_size_width()
        height = self.get_window_size_height()

        for i in range(num):
            self.driver.swipe(width * 0.25, height * 0.5, width * 0.75, height * 0.5, 7000)
            logger.info('swipe to rigth %s times' % i)

    def get_screen_shot(self):
        file_path = os.path.abspath('.') + "/screen_shot/"
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        screen_name = file_path + rq + '.png'
        try:
            self.driver.get_screenshot_as_file(screen_name)
            logger.info("Had take screenshot and save to folder : /screen_shot")
            logger.info("screen_shot name is %s" % screen_name)
        except NameError as e:
            logger.error("Failed to take screenshot! %s" % e)
            self.dirver.save_screenshot(screen_name)

    def install_app(self, app):
        try:
            self.driver.install_app(app)
        except:
            logger.error("install app failed")

    def remove_app(self, app):
        if self.is_app_installed(app):
            self.driver.remove_app(app)
        else:
            self.driver.install_app(app)
            self.driver.remove_app(app)

    def is_app_installed(self, app):
        return self.driver.is_app_installed(app)

    def launch_app(self):
        self.driver.launch_app()

    def find_element(self, value):
        return self.driver.find_element_by_id(value)

    def find_toast(self, message):
        toast_loc = ("xpath", ".//*[contains(@text,'%s')]" %message)
        try:
            element = WebDriverWait(self.driver, 5, 0.1).until(
                EC.presence_of_element_located(toast_loc))
            return True
        except:
            logger.error('cannot find %s' %message)
            return False
