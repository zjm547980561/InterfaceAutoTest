# -*- coding:utf-8 -*-
from framework.base import Base
regist_element = {
    'regist_btn': 'register_tx',
    'search_school': 'search_ex',
    'send_verify': 'send_verify',
    'msg': 'verify_ex',
    'name': 'name',
    'time_item': 'item',
    'next': 'next_tx',
    'phone': 'mobile_ex',
    'passwd': 'password_ex',
    'verify_msg': 'verify_ex',
    'confirm_btn': 'confirm_tx',
    'login': 'login_tx'
}

regist_toast_msg = {
    'short_passwd': u'密码过短，请重新输入密码',
    'registed': u'该手机号已经被注册，请直接登录！',
    'bad_number': u'请输入正确手机号码',
    'empty_number': u'请输入手机号码',
    'empty_passwd': u'请输入密码',
    'wrong_msg': u'验证码无效，请重新获取',
    'empty_msg': u'请输入验证码',
    'msg_success': u'发送成功'
}

regist_msg_data = {
    'phone': '18201010000',
    'bad_phone': '23456789012',
    'short_passwd': '1234',
    'long_passwd': '1234567890123456789',
    'passwd': '123456',
    'wrong_msg': '0000',
    'unregist': '15555555555',
    'empty_phone': '',
    'empty_passwd': '',
    'school_exist': '北京科技大学天津学院',
    'school_not_exist': '1234'
}


class Regist(Base):
    pass