# -*- coding:utf-8 -*-
from appium import webdriver
from framework.base import Base
from framework.logger import Logger
from config.remote_url import driver
from config.desired_caps import desired_caps
from framework.HTMLTestRunner import HTMLTestRunner

logger = Logger('runner').get_logger()

# import unittest
# import time


driver = Base(driver)
# driver.start_activity('fm.jihua.kecheng', '.ui.guide.GuideActivity')
logger.info('app removed')
driver.remove_app(desired_caps['appPackage'])
install = driver.is_app_installed(desired_caps['appPackage'])

print(install)
driver.install_app(desired_caps['app'])
install = driver.is_app_installed(desired_caps['appPackage'])

print(install)
driver.launch_app()
driver.get_screen_shot()
driver.swipe_left(4)
# print(driver.find_element_by_id('image'))