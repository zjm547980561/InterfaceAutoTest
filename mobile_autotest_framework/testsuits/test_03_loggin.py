# -*- coding:utf-8 -*-
import unittest
import logging
import time
from objects.loggin import loggin_toast_msg, loggin_element, loggin_data, Loggin
from config.desired_caps import uri, desired_caps


logger = logging.getLogger('ClassBox')


# @unittest.skip('')
class LogginTest(unittest.TestCase):
    #启动app
    @classmethod
    def setUpClass(cls):
        logger.info("<<<<<<<<<<<<<3，登录功能测试正式开始>>>>>>>>>>>>")
        cls.driver = Loggin(uri, desired_caps)
        # time.sleep(60)
        try:
            logger.info("    正在启动app")
            cls.driver.launch_app()
            time.sleep(5)
        except Exception as e:
            logger.info("    app启动失败")
            logger.error(e)
            cls.driver.quit()


    #测试输入超过11位以1开头的号码
    @Loggin.get_shot
    # @unittest.skip('')
    def test_01_long_number(self):
        logger.info('1，测试账号为11位以上的手机号')
        time.sleep(2)
        self.driver.login(loggin_element, loggin_data['long_phone'], loggin_data['passwd'])
        a = self.driver.find_toast(loggin_toast_msg['long_number'], loggin_element['confirm'])
        self.assertTrue(a)

    # 测试手机号输入为空
    @Loggin.get_shot
    # @unittest.skip('')
    def test_02_empty_number(self):
        logger.info('2，测试账号输入为空')
        time.sleep(2)
        self.driver.login(loggin_element, loggin_data['empty_phone'], loggin_data['passwd'])
        a = self.driver.find_toast(loggin_toast_msg['empty_number'], loggin_element['confirm'])
        self.assertTrue(a)

    # 测试11位非手机号
    @Loggin.get_shot
    # @unittest.skip('')
    def test_03_bad_number(self):
        logger.info('3，测试11位非手机号')
        time.sleep(2)
        self.driver.login(loggin_element, loggin_data['bad_phone'], loggin_data['passwd'])
        a = self.driver.find_toast(loggin_toast_msg['bad_number'], loggin_element['confirm'])
        self.assertTrue(a)

    # 测试未注册的手机号
    @Loggin.get_shot
    def test_04_01_unregist_number(self):
        logger.info('4-1，测试未注册的手机号, 点击弹窗"换个号码"')
        time.sleep(2)
        self.driver.login(loggin_element, loggin_data['unregist'], loggin_data['passwd'])
        self.driver.click_btn(loggin_element['confirm'])
        logger.info("    点击'换个号码'")
        self.driver.click_btn('cancel')
        a = self.driver.current_activity
        self.assertEqual(a, '.ui.register.RegisterActivity')

    @Loggin.get_shot
    def test_04_02_unregist_number(self):
        logger.info('4-2，测试未注册的手机号, 点击弹窗"立即注册"')
        time.sleep(2)
        self.driver.login(loggin_element, loggin_data['unregist'], loggin_data['passwd'])
        self.driver.click_btn(loggin_element['confirm'])
        logger.info("    点击'换个号码'")
        self.driver.click_btn('confirm')
        a = self.driver.current_activity
        self.driver.click_btn(loggin_data['login'])
        self.assertEqual(a, '.ui.register.SignUpActivity')

    # 测试账号输入框的快捷清除按钮
    @Loggin.get_shot
    # @unittest.skip('')
    def test_05_quick_clear_number(self):
        logger.info('5，测试账号输入框的快捷清除按钮')
        time.sleep(2)
        self.driver.send_data_to_element(loggin_element['phone'], '123456')
        self.driver.quick_clear(loggin_element['phone'])
        self.driver.quick_clear(loggin_element['phone'])
        a = self.driver.get_text(loggin_element['phone'])
        self.assertEqual('请输入手机号或格子号', a)

    # 测试密码输入框的快捷清除按钮
    @Loggin.get_shot
    # @unittest.skip('')
    def test_06_quick_clear_passwd(self):
        logger.info('6，测试密码输入框的快捷清除按钮')
        time.sleep(2)
        self.driver.send_data_to_element(loggin_element['passwd'], '123456')
        self.driver.quick_clear(loggin_element['passwd'])
        self.driver.quick_clear(loggin_element['passwd'])
        a = self.driver.get_text(loggin_element['passwd'])
        self.assertEqual('请输入密码', a)

    # 测试密码长度小于6位
    @Loggin.get_shot
    # @unittest.skip('')
    def test_06_short_passwd(self):
        logger.info('6，测试密码长度小于6')
        time.sleep(2)
        self.driver.login(loggin_element, loggin_data['phone'], loggin_data['short_passwd'])
        a = self.driver.find_toast(loggin_toast_msg['short_passwd'], loggin_element['confirm'])
        self.assertTrue(a)

    #测试密码错误
    @Loggin.get_shot
    # @unittest.skip('')
    def test_07_bad_passwd(self):
        logger.info('7，测试密码错误')
        time.sleep(2)
        self.driver.login(loggin_element, loggin_data['phone'], loggin_data['wrong_passwd'])
        a = self.driver.find_toast(loggin_toast_msg['bad_passwd'], loggin_element['confirm'])
        self.assertTrue(a)

    #测试密码输入为空
    @Loggin.get_shot
    # @unittest.skip('')
    def test_08_empty_passwd(self):
        logger.info('8，测试密码为空')
        time.sleep(2)
        self.driver.login(loggin_element, loggin_data['phone'])
        a = self.driver.find_toast(loggin_toast_msg['empty_passwd'], loggin_element['confirm'])
        self.assertTrue(a)

    # 测试密码明文显示
    @Loggin.get_shot
    # @unittest.skip('')
    def test_09_passwd_display(self):
        logger.info('9，测试密码明文显示')
        time.sleep(2)
        self.driver.login(loggin_element, loggin_data['phone'], passwd='123456')
        self.driver.click_btn(loggin_element['hide_passwd'])
        a = self.driver.get_text(loggin_element['passwd'])
        b = '123456'
        self.assertEqual(a, b)

    def test_10_passwd_display(self):
        logger.info('10，测试密码密文显示')
        time.sleep(2)
        self.driver.click_btn(loggin_element['hide_passwd'])
        a = self.driver.get_text(loggin_element['passwd'])
        b = '••••••'

        self.assertEqual(a, b)

    #测试第三方登录,没有绑定账号
    # @Loggin.get_shot
    @unittest.skip('')
    def test_08_third_part_loggin(self):
        logger.info('8，测试第三方登录,绑定账号')
        time.sleep(2)
        self.driver.find_element_by_id(loggin_element['third_part'][2]).click()
        time.sleep(5)
        a = self.driver.current_activity
        self.assertEqual(a, '.ui.home.HomeActivity')

    #测试第三方登录,没有绑定账号
    # @Loggin.get_shot
    # def test_09_third_part_loggin(self):
    #     logger.info('9，测试第三方登录完成后的注册工作,')
    #     time.sleep(2)
    #     self.driver.find_element_by_id(loggin_element['third_part'][0]).click()
    #     a = self.driver.find_toast(loggin_toast_msg['third_part'], loggin_element['confirm'])
    #     self.assertTrue(a)

    # 测试登录成功

    # @unittest.skip('')
    @Loggin.get_shot
    def test_11_loggin_success(self):
        time.sleep(2)
        logger.info('11，测试登录成功')
        self.driver.login(loggin_element, loggin_data['phone'], loggin_data['passwd'], success=True)
        time.sleep(2)
        logger.info("    进入'首页'")
        a = self.driver.current_activity
        self.assertEquals(a, '.ui.home.HomeActivity')

    # 测试登录成功
    @Loggin.get_shot
    # @unittest.skip('')
    def test_12_logout_success(self):
        time.sleep(5)
        logger.info('12，测试退出登录成功')
        self.driver.logout()
        logger.info("    进入'登录'")
        a = self.driver.current_activity
        self.assertEquals(a, '.ui.register.RegisterActivity')

    @classmethod
    def tearDownClass(cls):
        logger.info('<<<<<<<<<<<<<<<<<登录功能测试完成>>>>>>>>>>>>>>>>>>')
        cls.driver.quit()