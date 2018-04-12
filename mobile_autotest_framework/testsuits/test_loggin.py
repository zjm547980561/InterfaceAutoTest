# -*- coding:utf-8 -*-
import unittest
from framework.logger import Logger
from config.desired_caps import desired_caps, uri
from framework.driver import driver
from objects.loggin import loggin_element, loggin_data, loggin_toast_msg
import time
from appium import webdriver
from framework.base import Base

logger = Logger('test loggin').get_logger()
driver = Base(webdriver.Remote(uri, desired_caps))

# 装饰器，断言失败的时候会打印错误日志
def get_shot(func):
    def dec(*args):
        try:
            func(*args)
        except AssertionError as e:
            # driver.get_screen_shot()
            logger.error(e)
            raise AssertionError
        except Exception as e:
            logger.error(e)
            # driver.get_screen_shot()
            raise Exception
    return dec


# @unittest.skip('')
class Loggin(unittest.TestCase):
    #删除app，安装app，启动app
    @classmethod
    def setUpClass(cls):
        cls.driver = driver
        time.sleep(5)
        cls.driver.remove_app(desired_caps['appPackage'])
        cls.driver.install_app(desired_caps['app'])
        cls.driver.launch_app()
        time.sleep(3)

    #输入登录信息
    def login(self, phone, passwd):
        self.driver.find_element(loggin_element['phone']).clear().send_keys(phone)
        self.driver.find_element(loggin_element['passwd']).clear().send_keys(passwd)
        self.driver.find_element(loggin_element['confirm']).click()

    #测试输入超过11位以1开头的号码
    @get_shot
    def test_long_number(self):
        self.login(loggin_data['long_phone'], loggin_data['passwd'])
        a = self.driver.find_toast(loggin_toast_msg['long_number'])
        self.assertTrue(a)

    #测试密码长度小于6位
    @get_shot
    def test_short_passwd(self):
        self.login(loggin_data['phone'], loggin_data['short_passwd'])
        a = self.driver.find_toast(loggin_toast_msg['short_passwd'])
        self.assertTrue(a)

    #测试密码错误
    @get_shot
    def test_bad_passwd(self):
        self.login(loggin_data['phone'], loggin_data['wrong_passwd'])
        a = self.driver.find_toast(loggin_toast_msg['bad_passwd'])
        self.assertTrue(a)

    #测试未注册的手机号
    @get_shot
    def test_unregist_number(self):
        self.login(loggin_data['unregist'], loggin_data['passwd'])
        a = self.driver.find_toast(loggin_toast_msg['unregist'])
        self.assertTrue(a)

    #测试11位非手机号
    @get_shot
    def test_bad_number(self):
        self.login(loggin_data['bad_phone'], loggin_data['passwd'])
        a = self.driver.find_toast(loggin_toast_msg['bad_number'])
        self.assertTrue(a)

    #测试手机号输入为空
    @get_shot
    def test_empty_number(self):
        self.login(loggin_data['empty_phone'], loggin_data['passwd'])
        a = self.driver.find_toast(loggin_toast_msg['empty_number'])
        self.assertTrue(a)

    #测试密码输入为空
    @get_shot
    def test_empty_passwd(self):
        self.login(loggin_data['phone'], loggin_data['empty_passwd'])
        a = self.driver.find_toast(loggin_toast_msg['empty_passwd'])
        self.assertTrue(a)

    #测试登录成功
    @unittest.skip('')
    def test_loggin_success(self):
        self.login(loggin_data['phone'], loggin_data['passwd'])
        a = self.driver.current_activity
        self.assertEquals(a, '.ui.home.HomeActivity')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()