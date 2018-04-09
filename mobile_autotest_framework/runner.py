# -*- coding:utf-8 -*-
from framework.logger import Logger
from framework.HTMLTestRunner import HTMLTestRunner
import unittest
import time
import os

logger = Logger('RunScript').get_logger()

report_path = os.path.abspath('.') + '/test_reports/'

# 获取系统当前时间
now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))

# 设置报告名称格式
HtmlFile = report_path + now + "HTMLtemplate.html"
fp = open(HtmlFile, "wb")

# 构建suite
suite = unittest.TestLoader().discover(os.path.abspath('.') + '/testsuits')

if __name__ == '__main__':
    # 初始化一个HTMLTestRunner实例对象，用来生成报告
    logger.info('test begin')
    runner = HTMLTestRunner(stream=fp, title=u"课程格子项目测试报告", description=u"测试app的安装和卸载", verbosity=2)
    # 开始执行测试套件
    runner.run(suite)
    logger.info('test finished')
    fp.close()