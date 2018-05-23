# -*- coding:utf-8 -*-
from framework.base import Base
el = {
    'phone': 'mobile_ex',
    'passwd': 'password_ex',
    'confirm': 'confirm_tx'
}
data = {
    'phone': '15201418408',
    'passwd': '123456',
}

setting_element = {
    'setting': 'setting_iv',
    'account': 'account_setting',
    'back': 'left_layout',
    'passwd': {
        'passwd': 'password_layout',
        'old': 'old_password_ex',
        'new': 'new_password_ex',
        'verify_new': 'confirm_password_ex',
        'confirm_btn': 'right_layout',
        'back': 'left_layout'
    },
    'phone': {
        'phone': 'mobile_layout',
        'new_phone': 'mobile_ex',
        'verify_msg': 'verify_ex',
        'verify_btn': 'send_verify',
        'confirm_btn': 'confirm_tx'
    }
}

setting_data = {
    'phone': '15201418408',
    'old_passwd': '123456',
    'new_passwd': '1234567'
}

setting_toast_msg = {
    'wrong_new_passwd': u'两次输入的密码不一致',
    'wrong_old_passwd': u'原密码输入错误，请确认后重新输入。',
    'empty_old_passwd': u'原密码不能为空',
    'empty_new_passwd': u'新密码不能为空',
    'empty_verify_passwd': u'确认密码不能为空',
    'modify_success': u'修改成功，请重新登录',
    'empty_number': u'请输入手机号码',
    'registed_number': u'该手机已经被绑定',
    'bad_number': u'请输入正确手机号码',
    'wrong_msg': u'验证码输入错误，请更正后再次提交！',
    'empty_msg': u'验证码不能为空',
    'binging_success': u'手机号绑定成功',
    'short_passwd': u'密码不能少于6位',
    'long_passwd': u'密码长度太长'
}


class SettingModify(Base):
    pass

