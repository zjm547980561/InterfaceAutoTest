# -*- coding:utf-8 -*-
import unittest
from framework.logger import Logger
from config.desired_caps import desired_caps, uri
from framework.driver import driver
from objects.get_passwd_back import forget_passwd_element, forget_message_toast_msg, forget_msg_data
import time
from appium import webdriver
from framework.base import Base

logger = Logger('forget password').get_logger()
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
class GetPasswdBack(unittest.TestCase):
    #进入找回密码页面
    @classmethod
    def setUpClass(cls):
        cls.driver = driver
        cls.driver.launch_app()
        time.sleep(3)
        cls.driver.find_element(forget_passwd_element['forget_password']).click()
        cls.driver.find_element(forget_passwd_element['mobile_password']).click()
        time.sleep(2)

    # 输入登录信息
    def login(self, phone, passwd, msg=''):
        self.driver.find_element(forget_passwd_element['phone']).clear().send_keys(phone)
        time.sleep(2)
        self.driver.find_element(forget_passwd_element['msg']).clear().send_keys(msg)
        self.driver.find_element(forget_passwd_element['passwd']).clear().send_keys(passwd)
        self.driver.find_element(forget_passwd_element['confirm']).click()

    # 测试密码长度小于6位
    @get_shot
    def test_short_passwd(self):
        self.login(forget_msg_data['phone'], forget_msg_data['short_passwd'])
        a = self.driver.find_toast(forget_message_toast_msg['short_passwd'])
        self.assertTrue(a)

    # # 测试未注册的手机号
    # @get_shot
    # def test_unregist_number(self):
    #     self.driver.find_element(forget_passwd_element['phone']).clear().send_keys(forget_msg_data['unregist'])
    #     self.driver.find_element(forget_passwd_element['send_verify']).click()
    #     a = self.driver.find_toast(forget_message_toast_msg['unregist'])
    #     self.assertTrue(a)
    #
    # 测试非法手机号
    @get_shot
    def test_bad_number(self):
        self.login(forget_msg_data['bad_phone'], forget_msg_data['passwd'])
        a = self.driver.find_toast(forget_message_toast_msg['bad_number'])
        self.assertTrue(a)
    #
    # # 测试手机号输入为空
    @get_shot
    def test_empty_number(self):
        self.login(forget_msg_data['empty_phone'], forget_msg_data['passwd'])
        a = self.driver.find_toast(forget_message_toast_msg['empty_number'])
        self.assertTrue(a)
    #
    # # 测试密码输入为空
    @get_shot
    def test_empty_passwd(self):
        self.login(forget_msg_data['phone'], forget_msg_data['empty_passwd'])
        a = self.driver.find_toast(forget_message_toast_msg['empty_passwd'])
        self.assertTrue(a)
    #
    # # 测试验证码错误
    @get_shot
    def test_wrong_message(self):
        self.login(forget_msg_data['phone'], forget_msg_data['passwd'], forget_msg_data['wrong_msg'])
        a = self.driver.find_toast(forget_message_toast_msg['wrong_msg'])
        self.assertTrue(a)
    #
    # # 测试验证码输入为空
    @get_shot
    def test_empty_msg(self):
        self.login(forget_msg_data['phone'], forget_msg_data['passwd'])
        a = self.driver.find_toast(forget_message_toast_msg['empty_msg'])
        self.assertTrue(a)

    @classmethod
    def tearDownClass(cls):
        # pass
        cls.driver.quit()