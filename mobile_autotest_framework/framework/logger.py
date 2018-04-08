# -*- coding:utf-8 -*-
import logging
import time
import os


class Logger(object):
    def __init__(self, logger):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        log_path = os.path.abspath('.').rsplit('/', 1)[0] + '/log/'
        log_name = log_path + rq + '.log'
        handler = logging.FileHandler(log_name)
        handler.setLevel(logging.INFO)
        formtter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formtter)
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger