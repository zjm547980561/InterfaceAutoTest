# -*- coding:utf-8 -*-

from framework.logger import Logger
import os
import time
logger = Logger('base').get_logger()


class Base(object):
    def __init__(self, driver):
        self.driver = driver

    def quit(self):
        logger.info('quit success')
        self.driver.quit()

    def get_window_size_width(self):
        return self.driver.get_window_size()['width']

    def get_window_size_height(self):
        return self.driver.get_window_size()['height']

    def swipe_left(self, num):
        width = self.get_window_size_width()
        height = self.get_window_size_height()

        for i in range(num):
            self.driver.swipe(width * 0.75, height * 0.5, width * 0.25, height * 0.5, 4000)
            logger.info('swipe to left %s times' % (num + 1))

    def swipe_right(self, num):
        width = self.get_window_size_width()
        height = self.get_window_size_height()
        logger.info('swipe to rigth %s times' % num)
        for i in range(num):
            self.driver.swipe(width * 0.25, height * 0.5, width * 0.75, height * 0.5, 4000)
            # self.get_screen_shot()

    def get_screen_shot(self):
        file_path = os.path.abspath('.').rsplit('/', 1)[0] + "/screen_shot/"
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        screen_name = file_path + rq + '.png'
        # print(screen_name)
        try:
            self.driver.get_screenshot_as_file(screen_name)
            logger.info("Had take screenshot and save to folder : /screen_shot")
            logger.info("screen_shot name is s" % screen_name)
        except NameError as e:
            logger.error("Failed to take screenshot! %s" % e)
            self.dirver.save_screenshot(screen_name)

    def install_app(self, app):
        self.driver.install_app(app)

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
