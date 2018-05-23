# -*- coding:utf-8 -*-
'''
本脚本主要测试修改密码和改变绑定的手机号
    1，测试原密码为空
    2，测试新密码为空
    3，测试确认密码为空
    4，测试原密码错误
    5，测试两次密码输入不一致
    6，测试密码修改成功
    7，测试验证用新密码登录成功，再将新密码改成旧密码
    8，测试修改绑定的手机号为空
    9，测试修改新手机号已注册
    10，测试非法手机号
    11，测试验证码为空
    12，测试验证码错误
    13，测试修改绑定手机号成功（skip）
'''

import unittest
import logging
from objects.setting_profile import setting_data, setting_element, setting_toast_msg, SettingModify, el, data
import time
from config.desired_caps import uri, desired_caps

logger = logging.getLogger('ClassBox')


# @unittest.skip('')
class SettingProfile(unittest.TestCase):
    # 进入找回密码页面
    @classmethod
    def setUpClass(cls):
        logger.debug("<<<<<<<<<<<<<<<5，修改账号密码测试正式开始>>>>>>>>>>>>>>")
        cls.driver = SettingModify(uri, desired_caps)
        try:
            cls.driver.launch_app()
            logger.info("    正在启动app")
            time.sleep(5)
            if cls.driver.current_activity == '.ui.register.RegisterActivity':
                cls.driver.login(el, data['phone'], data['passwd'], success=True)
            cls.driver.my_page()
            time.sleep(1)
            logger.info("    点击设置按钮")
            cls.driver.click_btn('setting_iv')
            time.sleep(1)
        except Exception as e:
            logger.error(e)
            logger.info('    app启动失败')
            cls.driver.quit()

    # 测试原密码为空
    @SettingModify.get_shot
    def test_01_empty_old_passwd(self):
        logger.info('1, 测试原密码为空')
        logger.info("    点击账户按钮")
        self.driver.click_btn(setting_element['account'])
        time.sleep(1)
        logger.info("    点击密码按钮")
        self.driver.click_btn(setting_element['passwd']['passwd'])
        time.sleep(1)
        logger.info("    点击保存按钮")
        self.driver.click_btn('right_layout')
        a = self.driver.find_toast(setting_toast_msg['empty_old_passwd'], setting_element['passwd']['confirm_btn'])
        self.assertTrue(a)

    # 测试新密码为空
    @SettingModify.get_shot
    def test_02_empty_new_passwd(self):
        logger.info('2, 测试新密码为空')
        logger.info("    输入旧密码：abcdef" )
        self.driver.send_data_to_element(setting_element['passwd']['old'], 'abcdef')
        a = self.driver.find_toast(setting_toast_msg['empty_new_passwd'], setting_element['passwd']['confirm_btn'])
        self.assertTrue(a)

    # 测试确认密码为空
    @SettingModify.get_shot
    def test_03_empty_verify_passwd(self):
        logger.info('3, 测试确认密码为空')
        logger.info("    输入旧密码：abcdef")
        self.driver.send_data_to_element(setting_element['passwd']['old'], 'abcdef')
        logger.info("    输入新密码：abcdef")
        self.driver.send_data_to_element(setting_element['passwd']['new'], 'abcdef')
        a = self.driver.find_toast(setting_toast_msg['empty_verify_passwd'], setting_element['passwd']['confirm_btn'])
        self.assertTrue(a)

    # 测试原密码错误
    @SettingModify.get_shot
    def test_04_wrong_old_passwd(self):
        logger.info('4, 测试原密码错误')
        logger.info("    输入旧密码：abcdef")
        self.driver.send_data_to_element(setting_element['passwd']['old'], 'abcdef')
        logger.info("    输入新密码：abcdef")
        self.driver.send_data_to_element(setting_element['passwd']['new'], 'abcdef')
        logger.info("    输入验证新密码：abcdef")
        self.driver.send_data_to_element(setting_element['passwd']['verify_new'], 'abcdef')
        a = self.driver.find_toast(setting_toast_msg['wrong_old_passwd'], setting_element['passwd']['confirm_btn'])
        self.assertTrue(a)

    # 测试密码长度小于6位
    @SettingModify.get_shot
    def test_05_short_passwd(self):
        logger.info('5, 测试密码长度小于6位')
        logger.info("    输入新密码：abc")
        self.driver.send_data_to_element(setting_element['passwd']['new'], 'abc')
        self.driver.send_data_to_element(setting_element['passwd']['verify_new'], 'abc')
        a = self.driver.find_toast(setting_toast_msg['short_passwd'], setting_element['passwd']['confirm_btn'])
        self.assertTrue(a)

    # 测试密码长度不大于18位
    @SettingModify.get_shot
    def test_06_long_passwd(self):
        logger.info('6, 测试密码长度不大于18位')
        logger.info("    输入新密码：1234567890123456789")
        self.driver.send_data_to_element(setting_element['passwd']['old'], '123456')
        self.driver.send_data_to_element(setting_element['passwd']['new'], '1234567890123456789')
        self.driver.send_data_to_element(setting_element['passwd']['verify_new'], '1234567890123456789')
        a = self.driver.find_toast(setting_toast_msg['long_passwd'], setting_element['passwd']['confirm_btn'])
        self.assertTrue(a)

    # 测试两次密码输入不一致
    @SettingModify.get_shot
    def test_07_wrong_new_passwd(self):
        logger.info('7, 测试两次密码输入不一致')
        logger.info("    输入旧密码：abcdef")
        self.driver.send_data_to_element(setting_element['passwd']['old'], 'abcdef')
        logger.info("    输入新密码：abcdef")
        self.driver.send_data_to_element(setting_element['passwd']['new'], 'abcdef')
        logger.info("    输入验证密码：abcdefg")
        self.driver.send_data_to_element(setting_element['passwd']['verify_new'], 'abcdefg')
        a = self.driver.find_toast(setting_toast_msg['wrong_new_passwd'], setting_element['passwd']['confirm_btn'])
        self.assertTrue(a)

    # 测试密码修改成功
    @SettingModify.get_shot
    def test_08_modify_success(self):

        logger.info('8, 测试密码修改成功')
        logger.info("    输入旧密码：%s" % setting_data['old_passwd'])
        self.driver.send_data_to_element(setting_element['passwd']['old'], setting_data['old_passwd'])
        logger.info("    输入新密码：%s" % setting_data['new_passwd'])
        self.driver.send_data_to_element(setting_element['passwd']['new'], setting_data['new_passwd'])
        logger.info("    输入验证新密码：%s" % setting_data['new_passwd'])
        self.driver.send_data_to_element(setting_element['passwd']['verify_new'], setting_data['new_passwd'])
        a = self.driver.find_toast(setting_toast_msg['modify_success'], setting_element['passwd']['confirm_btn'])
        logger.info('    修改后的密码为 %s' % setting_data['new_passwd'])
        self.assertTrue(a)

    #测试验证用新密码登录成功
    @SettingModify.get_shot
    def test_09_01_loggin_success(self):

        logger.info('9-1, 测试验证新密码登录成功')
        time.sleep(2)
        self.driver.login(el, setting_data['phone'], setting_data['new_passwd'], success=True)
        time.sleep(2)
        logger.info("    登录成功后进入'首页'")
        a = self.driver.current_activity
        self.assertEquals(a, '.ui.home.HomeActivity')

    # 测试将新密码改为旧密码
    @SettingModify.get_shot
    def test_09_02_loggin_success(self):
        logger.info('9-2, 测试将新密码改为旧密码')
        logger.info("    进入'我的'页面")
        self.driver.my_page()
        time.sleep(1)
        logger.info("    点击设置按钮")
        self.driver.click_btn(setting_element['setting'])
        time.sleep(1)
        logger.info("    点击账户按钮")
        self.driver.click_btn(setting_element['account'])
        time.sleep(1)
        logger.info("    点击密码按钮")
        self.driver.click_btn(setting_element['passwd']['passwd'])
        time.sleep(1)
        logger.info("    输入旧密码：%s" % setting_data['new_passwd'])
        self.driver.send_data_to_element(setting_element['passwd']['old'], setting_data['new_passwd'])
        logger.info("    输入新密码：%s" % setting_data['old_passwd'])
        self.driver.send_data_to_element(setting_element['passwd']['new'], setting_data['old_passwd'])
        logger.info("    输入验证新密码：%s" % setting_data['old_passwd'])
        self.driver.send_data_to_element(setting_element['passwd']['verify_new'], setting_data['old_passwd'])
        logger.info("    点击保存按钮")
        self.driver.click_btn('right_layout')
        time.sleep(2)
        self.driver.login(el, setting_data['phone'], setting_data['old_passwd'], success=True)
        logger.info("    更改完成之后进入'首页'")
        a = self.driver.current_activity
        self.assertEquals(a, '.ui.home.HomeActivity')

    #测试修改绑定的手机号为空
    @SettingModify.get_shot
    def test_10_empty_number(self):
        logger.info('10, 测试修改绑定的手机号为空')
        logger.info("    进入'我的'页面")
        self.driver.my_page()
        time.sleep(1)
        logger.info("    点击设置按钮")
        self.driver.click_btn(setting_element['setting'])
        time.sleep(1)
        logger.info("    点击账户按钮")
        self.driver.click_btn(setting_element['account'])
        time.sleep(1)
        logger.info("    点击手机号按钮")
        self.driver.click_btn(setting_element['phone']['phone'])
        time.sleep(1)
        a = self.driver.find_toast(setting_toast_msg['empty_number'], el['confirm'])
        self.assertTrue(a)


    #测试修改新手机号已注册
    @SettingModify.get_shot
    def test_11_registed_number(self):
        logger.info('11, 测试修改新手机号已注册')
        logger.info("    输入手机号：%s" % setting_data['phone'])
        self.driver.send_data_to_element(setting_element['phone']['new_phone'], setting_data['phone'])
        a = self.driver.find_toast(setting_toast_msg['registed_number'], setting_element['phone']['verify_btn'])
        self.assertTrue(a)

    #测试非法手机号
    @SettingModify.get_shot
    def test_12_bad_number(self):
        logger.info('12, 测试非法手机号')
        logger.info("    输入手机号：7829287")
        self.driver.send_data_to_element(setting_element['phone']['new_phone'], '7829287')
        a = self.driver.find_toast(setting_toast_msg['bad_number'], setting_element['phone']['confirm_btn'])
        self.assertTrue(a)

    #测试验证码为空
    @SettingModify.get_shot
    def test_13_empty_msg(self):
        logger.info('13, 测试验证码为空')
        logger.info("    输入手机号：%s" % setting_data['phone'])
        self.driver.send_data_to_element(setting_element['phone']['new_phone'], setting_data['phone'])
        a = self.driver.find_toast(setting_toast_msg['empty_msg'], setting_element['phone']['confirm_btn'])
        self.assertTrue(a)

    #测试验证码错误
    @SettingModify.get_shot
    def test_14_wrong_msg(self):
        logger.info('14, 测试验证码错误')
        logger.info("    输入手机号：%s" % setting_data['phone'])
        self.driver.send_data_to_element(setting_element['phone']['new_phone'], setting_data['phone'])
        logger.info("    输入验证码：1234")
        self.driver.send_data_to_element(setting_element['phone']['verify_msg'], '1234')
        a = self.driver.find_toast(setting_toast_msg['wrong_msg'], setting_element['phone']['confirm_btn'])
        self.assertTrue(a)

    #测试修改绑定手机号成功
    # @SettingModify.get_shot
    @unittest.skip('跳过本测试用例，不修改绑定的手机号')
    def test_15_phone_rebinding_success(self):
        logger.info('15, 测试修改绑定手机号成功')
        logger.info("    输入手机号：%s" % setting_data['phone'])
        self.driver.send_data_to_element(setting_element['phone']['new_phone'], setting_data['phone'])
        logger.info("    输入验证码：1234")
        self.driver.send_data_to_element(setting_element['phone']['verify_msg'], '1234')
        a = self.driver.find_toast(setting_toast_msg['binging_success'], setting_element['phone']['confirm_btn'])
        self.assertTrue(a)

    @classmethod
    def tearDownClass(cls):
        logger.info('<<<<<<<<<<<<<<<<<<<账号密码，绑定手机设置修改成功>>>>>>>>>>>>>>>')
        for i in range(3):
            logger.info("    点击后退按钮")
            cls.driver.click_btn(setting_element['back'])
            time.sleep(1)
        time.sleep(1)
        cls.driver.logout()
        cls.driver.quit()
