# -*- coding:utf-8 -*-
import configparser
import os


class AccountNumber(object):
    @property
    def get_value(self):
        config = configparser.ConfigParser()
        file_path = os.path.abspath('.') + '/config/config.ini'
        config.read(file_path)

        mobile = config.get("mobile", "value")
        passwd = config.get("passwd", "value")
        new_passwd = config.get("new_passwd", "value")
        unregisted = config.get("unregisted", "value")

        return (mobile, passwd, new_passwd, unregisted)


all_account = AccountNumber().get_value
