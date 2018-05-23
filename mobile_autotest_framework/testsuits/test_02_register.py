# -*- coding:utf-8 -*-
'''
本测试脚本实现了app的自动化注册
        1，测试注册跳转按钮
        2，测试学校搜索功能,搜索存在的学校
        3，测试学校搜索功能,搜索不存在的学校
        4，测试手机号为空
        5，测试非法手机号
        6，测试验证码为空
        7，测试密码为空
        8，测试注册密码长度小于6位
        9，测试注册成功（没有万能验证码所以无法注册成功）
        10，测试已存在账号直接登录
'''

import unittest
import logging
from objects.new_regist import regist_element, regist_msg_data, regist_toast_msg, Regist
import time
from config.desired_caps import desired_caps, uri

logger = logging.getLogger('ClassBox')


# @unittest.skip('')
class NewRegist(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.debug("<<<<<<<<<<<<<2，注册功能测试正式开始>>>>>>>>>>>>")
        cls.driver = Regist(uri, desired_caps)
        try:
            logger.info("    正在启动app")
            cls.driver.launch_app()
            logger.info("   进入注册页面")
            cls.driver.click_btn(regist_element['regist_btn'])
            time.sleep(5)
        except Exception as e:
            logger.info("    app启动失败")
            logger.error(e)
            cls.driver.quit()

    #测试注册phone为空
    @Regist.get_shot
    def test_01_empty_phone(self):
        logger.info('01,测试手机号为空')
        time.sleep(1)
        logger.info('    确认按钮不可点击')
        self.assertFalse(self.driver.find_element_by_id(regist_element['confirm_btn']).is_enabled())

    # 测试注册bad number
    @Regist.get_shot
    def test_02_bad_phone(self):
        logger.info('02,测试非法手机号')
        logger.info('    输入非法手机号 %s' % regist_msg_data['bad_phone'])
        self.driver.send_data_to_element(regist_element['phone'], regist_msg_data['bad_phone'])
        logger.info('    确认按钮不可点击')
        self.assertFalse(self.driver.find_element_by_id(regist_element['confirm_btn']).is_enabled())

    # 测试输入已注册手机号
    @Regist.get_shot
    # @unittest.skip('')
    def test_03_01_registed_number(self):
        logger.info('03-01,测试输入已注册手机号, 点击弹窗的"直接登录"，进入登录页面')
        logger.info('    输入手机号 %s' % regist_msg_data['phone'])
        self.driver.send_data_to_element(regist_element['phone'], regist_msg_data['phone'])
        logger.info("    点击发送验证码按钮，出现弹窗")
        self.driver.click_btn(regist_element['send_verify'])
        logger.info('    点击弹窗"立即登录"，进入登录页面')
        self.driver.click_btn('cancel')
        a = self.driver.current_activity
        logger.info("   点击立即注册，进入注册页面")
        self.driver.click_btn(regist_element['regist_btn'])
        self.assertEqual(a, '.ui.register.RegisterActivity')

    @Regist.get_shot
    # @unittest.skip('')
    def test_03_02_registed_number(self):
        logger.info('03-02,测试输入已注册手机号, 点击弹窗的"换个号码"，留在此页面')
        logger.info('    输入手机号 %s' % regist_msg_data['phone'])
        self.driver.send_data_to_element(regist_element['phone'], regist_msg_data['phone'])
        logger.info("    点击发送验证码按钮")
        self.driver.click_btn(regist_element['send_verify'])
        self.driver.click_btn('confirm')
        a = self.driver.current_activity
        self.assertEqual(a, '.ui.register.SignUpActivity')

    # 测试验证码发送成功
    @Regist.get_shot
    # @unittest.skip('')
    def test_04_01_msg_send_success(self):
        logger.info('04-01, 测试验证码发送成功，发送周期为60s')
        logger.info('    输入手机号 %s' % regist_msg_data['unregist'])
        self.driver.send_data_to_element(regist_element['phone'], regist_msg_data['unregist'])
        a = self.driver.find_toast(regist_toast_msg['msg_success'], regist_element['send_verify'])
        self.assertTrue(a)

    @Regist.get_shot
    # @unittest.skip('')
    def test_04_02_msg_send_success(self):
        logger.info('04-02, 测试验证码发送成功，发送周期为60s')
        logger.info('    点击获取验证码后，该按钮text发生变化')
        b = self.driver.get_text(regist_element['send_verify'])
        self.assertIn("重新获取", b)

    @Regist.get_shot
    # @unittest.skip('')
    def test_04_03_msg_send_success(self):
        logger.info('04-03, 测试验证码发送成功，发送周期为60s')
        logger.info('    点击获取验证码后，该按钮变成不可点击')
        b = self.driver.find_element_by_id(regist_element['send_verify']).is_enabled()
        self.assertFalse(b)

    # 测试注册验证码为空
    @Regist.get_shot
    def test_06_empty_msg(self):
        logger.info('06, 测试验证码为空')
        logger.info('    输入手机号 %s' % regist_msg_data['unregist'])
        self.driver.send_data_to_element(regist_element['phone'], regist_msg_data['unregist'])
        logger.info('    输入密码 %s' % regist_msg_data['passwd'])
        self.driver.send_data_to_element(regist_element['passwd'], regist_msg_data['passwd'])
        logger.info('    确认按钮不可点击')
        self.assertFalse(self.driver.find_element_by_id(regist_element['confirm_btn']).is_enabled())

    # 测试验证码错误
    @Regist.get_shot
    def test_07_wrong_msg(self):
        logger.info('07, 测试验证码错误')
        logger.info('    输入手机号 %s' % regist_msg_data['unregist'])
        self.driver.send_data_to_element(regist_element['phone'], regist_msg_data['unregist'])
        logger.info('    输入验证码 %s' % regist_msg_data['wrong_msg'])
        self.driver.send_data_to_element(regist_element['verify_msg'], regist_msg_data['wrong_msg'])
        logger.info('    输入密码 %s' % regist_msg_data['passwd'])
        self.driver.send_data_to_element(regist_element['passwd'], regist_msg_data['passwd'])

        a = self.driver.find_toast(regist_toast_msg['wrong_msg'], regist_element['confirm_btn'])
        self.assertTrue(a)

    # 测试注册密码为空
    @Regist.get_shot
    def test_08_empty_passwd(self):
        logger.info('08, 测试密码为空')
        logger.info('    输入手机号 %s' % regist_msg_data['unregist'])
        self.driver.send_data_to_element(regist_element['phone'], regist_msg_data['unregist'])
        logger.info('    清除密码')
        self.driver.clear_data(regist_element['passwd'])
        logger.info('    输入验证码 %s' % regist_msg_data['wrong_msg'])
        self.driver.send_data_to_element(regist_element['verify_msg'], regist_msg_data['wrong_msg'])
        logger.info('    确认按钮不可点击')
        self.assertFalse(self.driver.find_element_by_id(regist_element['confirm_btn']).is_enabled())

    # 测试注册密码长度小于6位
    @Regist.get_shot
    def test_09_short_passwd(self):
        logger.info('09, 测试注册密码长度小于6位')
        logger.info('    输入手机号 %s' % regist_msg_data['unregist'])
        self.driver.send_data_to_element(regist_element['phone'], regist_msg_data['unregist'])
        logger.info('    输入验证码 %s' % regist_msg_data['wrong_msg'])
        self.driver.send_data_to_element(regist_element['verify_msg'], regist_msg_data['wrong_msg'])
        logger.info('    输入密码 %s' % regist_msg_data['passwd'])
        self.driver.send_data_to_element(regist_element['passwd'], regist_msg_data['short_passwd'])
        logger.info('    确认按钮不可点击')
        self.assertFalse(self.driver.find_element_by_id(regist_element['confirm_btn']).is_enabled())

    # 测试密码长度大于18位
    @Regist.get_shot
    # @unittest.skip('')
    def test_10_long_passwd(self):
        logger.info('10, 测试密码长度大于18位')
        logger.info('    输入手机号 %s' % regist_msg_data['phone'])
        self.driver.send_data_to_element(regist_element['phone'], regist_msg_data['phone'])
        logger.info('    输入验证码 %s' % regist_msg_data['wrong_msg'])
        self.driver.send_data_to_element(regist_element['verify_msg'], regist_msg_data['wrong_msg'])
        logger.info('    输入密码 %s' % regist_msg_data['long_passwd'])
        self.driver.send_data_to_element(regist_element['passwd'], regist_msg_data['long_passwd'])
        logger.info('    确认按钮不可点击')
        self.assertFalse(self.driver.find_element_by_id(regist_element['confirm_btn']).is_enabled())

    # 测试已存在账号直接登录
    @Regist.get_shot
    def test_11_exist_account(self):
        logger.info('11, 测试已存在账号直接登录')
        logger.info("    点击已有账号按钮")
        self.driver.click_btn(regist_element['login'])
        time.sleep(2)
        a = self.driver.current_activity
        logger.info("    跳转到登录页面")
        self.driver.click_btn(regist_element['regist_btn'])
        logger.info('    点击"立即注册"跳转到注册页面')
        self.assertEqual(a, '.ui.register.RegisterActivity')

    # 测试注册成功
    # @Regist.get_shot
    @unittest.skip('无法得到正确的验证码')
    def test_12_regist_success(self):
        logger.info('12, 测试进入下一步')
        logger.info('    输入验证码 %s' % regist_msg_data['wrong_msg'])
        self.driver.send_data_to_element(regist_element['verify_msg'], regist_msg_data['wrong_msg'])
        logger.info('    输入密码 %s' % regist_msg_data['passwd'])
        self.driver.send_data_to_element(regist_element['passwd'], regist_msg_data['passwd'])
        logger.info("    进入下一步，完善学校信息")
        self.driver.click_btn(regist_element['confirm_btn'])
        a = self.driver.element_exist(regist_element['search_school'])
        self.assertTrue(a)

    # 测试学校搜索功能,搜索存在的学校
    @unittest.skip('')
    # @Regist.get_shot
    def test_13_search_school(self):
        logger.info('13, 测试搜索已存在的学校')
        logger.info('    输入要搜索的学校（存在）')
        self.driver.send_data_to_element(regist_element['search_school'], regist_msg_data['school_exist'])
        time.sleep(1)
        logger.info('    获取搜索结果')
        names = self.driver.find_elements_by_id(regist_element['name'])
        if regist_msg_data['school_exist'] in names[0].text:
            self.assertTrue(True)

    # 测试学校搜索功能,搜索不存在的学校
    @unittest.skip('')
    # @Regist.get_shot
    def test_14_search_school_not_exist(self):
        logger.info('14, 测试搜索不存在的学校')
        logger.info('    输入要搜索的学校（不存在）')
        self.driver.send_data_to_element(regist_element['search_school'], regist_msg_data['school_not_exist'])
        time.sleep(1)
        logger.info('    获取搜索结果')
        names = self.driver.find_elements_by_id(regist_element['name'])
        if len(names) == 1 and names[0].text == '其他学校':
            self.assertTrue(True)

    @classmethod
    def tearDownClass(cls):
        logger.info('    <<<<<<<<<<<<<<<<<注册功能测试完成>>>>>>>>>>>>>>>>>>')
        cls.driver.quit()