# -*- coding:utf-8 -*-
from framework.base import Base
import logging
loggin_element = {
    'phone': 'mobile_ex',
    'passwd': 'password_ex',
    'confirm': 'confirm_tx',
    'hide_passwd': 'hide_password_iv',
    'forget_password': 'forget_password_tx',
    'mobile_password': 'mobile_password',
    'send_verify': 'send_verify',
    'third_part': {
                    0: 'wechart_iv',
                    1: 'weibo_iv',
                    2: 'qq_iv',

    }
}

loggin_toast_msg = {
    'long_number': u'请输入正确手机号码或格子号',
    'short_passwd': u'密码过短，请重新输入密码',
    'bad_passwd': u'密码错误，请确认后重新登录',
    'unregist': u'该用户未注册，请先注册',
    'bad_number': u'请输入正确手机号码',
    'empty_number': u'请输入手机号或格子号',
    'empty_passwd': u'请输入密码',
    'third_part': u'新同学你好，请先完成注册'
}

loggin_data = {
    'phone': '15201418408',
    'bad_phone': '23456789012',
    'long_phone': '182010100000',
    'short_passwd': '1234',
    'passwd': '123456',
    'wrong_passwd': '123457',
    'unregist': '15678912345',
    'empty_phone': '',
    'empty_passwd': '',
    'login': 'login_tx'
}
logger = logging.getLogger("ClassBox")


class Loggin(Base):
    def is_regist_page(self):
        logger.info("   进入登录页面")
        return self.find_element_by_id(loggin_element['phone'])

    @property
    def is_confirm_enable(self):
        return self.find_element_by_id("confirm_tx").is_enabled()

