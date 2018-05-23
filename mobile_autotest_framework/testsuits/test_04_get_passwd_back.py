# -*- coding:utf-8 -*-
'''
本脚本注册测试找回密码功能，以及其他一些错误的情况
    1，测试密码长度小于6位
    2，测试未注册的手机号
    3，测试非法手机号
    4，测试手机号输入为空
    5，测试密码输入为空
    6，测试验证码错误
    7，测试验证码输入为空
    8，测试验证码长度为19位
    9，测试修改成功
    10，测试修改成功后登录成功
'''

import unittest
import logging
import time
from config.desired_caps import uri, desired_caps
from objects.get_passwd_back import forget_msg_data, forget_passwd_element, forget_message_toast_msg, ForgetPasswd

logger = logging.getLogger('ClassBox')


# @unittest.skip('')
class GetPasswdBack(unittest.TestCase):
    #进入找回密码页面
    @classmethod
    def setUpClass(cls):
        logger.debug("<<<<<<<<<<<<<4，找回密码功能测试正式开始>>>>>>>>>>>>")
        cls.driver = ForgetPasswd(command_executor=uri, desired_capabilities=desired_caps)
        try:
            cls.driver.launch_app()
            logger.info("    正在启动app")
            time.sleep(5)
            cls.driver.click_find_passwd()
            time.sleep(1)
            cls.driver.click_mobile_find()
            time.sleep(1)
        except Exception as e:
            logger.error(e)
            logger.info("    app启动失败")
            cls.driver.quit()

    # 测试未注册的手机号
    @ForgetPasswd.get_shot
    def test_01_unregist_number(self):
        logger.info('1，测试未注册的手机号')
        # 当验证码获取的次数> 10次时，此case会出错
        time.sleep(2)
        logger.info("    输入未注册的手机号：%s" % forget_msg_data['unregist'])
        self.driver.send_data_to_element(forget_passwd_element['phone'], forget_msg_data['unregist'])
        a = self.driver.find_toast(forget_message_toast_msg['unregist'], forget_passwd_element['send_verify'])
        self.assertTrue(a)

    # 测试非法手机号
    @ForgetPasswd.get_shot
    def test_02_bad_number(self):
        logger.info('2，测试非法手机号')
        time.sleep(2)
        self.driver.login(forget_passwd_element, forget_msg_data['bad_phone'], forget_msg_data['passwd'])
        a = self.driver.find_toast(forget_message_toast_msg['bad_number'], forget_passwd_element['confirm'])
        self.assertTrue(a)

    # # 测试手机号输入为空
    @ForgetPasswd.get_shot
    def test_03_empty_number(self):
        logger.info('3，测试手机号输入为空')
        time.sleep(2)
        self.driver.login(forget_passwd_element, forget_msg_data['empty_phone'], forget_msg_data['passwd'])
        a = self.driver.find_toast(forget_message_toast_msg['empty_number'], forget_passwd_element['confirm'])
        self.assertTrue(a)

    # 测试密码长度小于6位
    @ForgetPasswd.get_shot
    def test_04_short_passwd(self):
        logger.info('4，测试密码长度小于6位')
        time.sleep(2)
        self.driver.login(forget_passwd_element, forget_msg_data['phone'], forget_msg_data['short_passwd'])
        a = self.driver.find_toast(forget_message_toast_msg['short_passwd'], forget_passwd_element['confirm'])
        self.assertTrue(a)

    # # 测试密码输入为空
    @ForgetPasswd.get_shot
    def test_05_empty_passwd(self):
        logger.info('5，测试密码输入为空')
        time.sleep(2)
        self.driver.login(forget_passwd_element, forget_msg_data['phone'], forget_msg_data['empty_passwd'])
        a = self.driver.find_toast(forget_message_toast_msg['empty_passwd'], forget_passwd_element['confirm'])
        self.assertTrue(a)

    # # 测试验证码长度为19位
    @ForgetPasswd.get_shot
    def test_06_long_passwd(self):
        logger.info('6，测试验证码长度为19位')
        time.sleep(2)
        self.driver.login(forget_passwd_element, forget_msg_data['phone'], forget_msg_data['long_passwd'])
        a = self.driver.find_toast(forget_message_toast_msg['long_passwd'], forget_passwd_element['confirm'])
        self.assertTrue(a)

    # # 测试验证码错误
    @ForgetPasswd.get_shot
    def test_07_wrong_message(self):
        logger.info('7，测试验证码错误')
        time.sleep(2)
        logger.info("    输入手机号：%s" % forget_msg_data['phone'])
        self.driver.send_data_to_element(forget_passwd_element['phone'], forget_msg_data['phone'])
        time.sleep(2)
        logger.info("    输入验证码：%s" % forget_msg_data['wrong_msg'])
        self.driver.send_data_to_element(forget_passwd_element['msg'], forget_msg_data['wrong_msg'])
        time.sleep(2)
        logger.info("    输入密码：%s" % forget_msg_data['passwd'])
        self.driver.send_data_to_element(forget_passwd_element['passwd'],forget_msg_data['passwd'])
        a = self.driver.find_toast(forget_message_toast_msg['wrong_msg'], forget_passwd_element['confirm'])
        self.assertTrue(a)

    # # 测试验证码输入为空
    @ForgetPasswd.get_shot
    def test_08_empty_msg(self):
        logger.info('8，测试验证码输入为空')
        time.sleep(2)
        self.driver.login(forget_passwd_element, forget_msg_data['phone'], forget_msg_data['passwd'])
        logger.info("    清除验证码")
        self.driver.clear_data(forget_passwd_element['msg'])
        time.sleep(1)
        a = self.driver.find_toast(forget_message_toast_msg['empty_msg'], forget_passwd_element['confirm'])
        self.assertTrue(a)


    # # 测试修改成功
    # @ForgetPasswd.get_shot
    # def test_09_modify_success(self):
    #     logger.info('9，测试找回密码成功')
    #     time.sleep(2)
    #     self.driver.login(forget_passwd_element, forget_msg_data['phone'], forget_msg_data['modified_passwd'])
    #     self.driver.find_element_by_id(forget_passwd_element['msg']).clear().send_keys(forget_msg_data['correct_msg'])
    #     a = self.driver.find_toast(forget_message_toast_msg['modify_success'], forget_passwd_element['confirm'])
    #     logger.info("    找回账号后设定的密码为 %s" % forget_msg_data['modified_passwd'])
    #     self.assertTrue(a)

    # # 测试修改成功后登录成功
    # @ForgetPasswd.get_shot
    # def test_10_login_success(self):
    #     logger.info('10，测试修改密码后登录成功')
    #     time.sleep(2)
    #     self.driver.login(forget_passwd_element, forget_msg_data['phone'], forget_msg_data['modified_passwd'], success=True)
    #     a = self.driver.current_activity
    #     self.assertEquals(a, '.ui.home.HomeActivity')

    @classmethod
    def tearDownClass(cls):
        logger.info("<<<<<<<<<<<<<<<<<<<找回密码功能测试完毕>>>>>>>>>>>>>>>>>>>>>")
        # cls.driver.logout()
        cls.driver.quit()
