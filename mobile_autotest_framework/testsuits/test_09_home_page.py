# -*- coding:utf-8 -*-

import unittest
import logging
from objects.home_page import loggin_data, loggin_element
import time
from framework.base import Base
from config.desired_caps import uri, desired_caps

# my_driver = Base(command_executor=uri, desired_capabilities=desired_caps)
logger = logging.getLogger('ClassBox')


@unittest.skip('')
class HomePage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.debug("<<<<<<<<<<<<<5首页测试正式开始>>>>>>>>>>>>")
        cls.driver = Base(uri, desired_caps)
        cls.driver.launch_app()
        time.sleep(5)
        cls.driver.loggin_success(loggin_data['phone'], loggin_data['passwd'])

    @Base.get_shot
    def test_class_reminder(self):
        # 切换到首页
        self.driver.home_page()

        el = self.driver.find_element_by_id('course_card')
        title = el.find_element_by_id('title')
        data_time = el.find_element_by_id('time')
        slot = el.find_element_by_id('slot')
        course_name = el.find_element_by_id('course_name')
        course_time = el.find_element_by_id('course_time')

        self.assertIsNotNone(el)