# -*- coding:utf-8 -*-
import random
from framework.base import Base
import logging
num = random.randint(99999,999999)


forget_passwd_element = {
    'phone': 'mobile_ex',
    'passwd': 'password_ex',
    'confirm': 'confirm_tx',
    'forget_password': 'forget_password_tx',
    'mobile_password': 'mobile_password',
    'send_verify': 'send_verify',
    'msg': 'verify_ex'
}

forget_message_toast_msg = {
    'short_passwd': u'密码过短，请重新输入密码',
    'unregist': u'该手机尚未注册，请先注册！',
    'bad_number': u'请输入正确手机号码',
    'empty_number': u'请输入手机号码',
    'empty_passwd': u'请输入密码',
    'wrong_msg': u'验证码输入错误，请更正后再次提交！',
    'empty_msg': u'请输入验证码',
    'modify_success': u'密码重置成功',
    'long_passwd': u'密码过长，请重新输入密码'
}

forget_msg_data = {
    'phone': '15201418408',
    'bad_phone': '23456789012',
    'short_passwd': '1234',
    'passwd': '123456',
    'wrong_msg': '0000',
    'unregist': '15555555555',
    'empty_phone': '',
    'empty_passwd': '',
    'correct_msg': '1234',
    'modified_passwd': str(num),
    'long_passwd': '1234567890123456789'
}

logger = logging.getLogger("ClassBox")


class ForgetPasswd(Base):
    def click_find_passwd(self):
        logger.info("   点击忘记密码")
        self.click_btn(forget_passwd_element['forget_password'])

    def click_mobile_find(self):
        logger.info("   点击手机找回密码")
        self.click_btn(forget_passwd_element['mobile_password'])
