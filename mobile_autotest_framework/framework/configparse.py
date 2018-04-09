# -*- coding:utf-8 -*-
import configparser
import os


class ReadConfigFile(object):

    def get_value(self):
        config = configparser.ConfigParser()
        file_path = os.path.dirname(os.path.abspath('.')) + '/config/config.ini'
        config.read(file_path)

        mobile = config.get("mobile", "value")
        passwd = config.get("passwd", "value")

        return (mobile, passwd)

