# -*- coding:utf-8 -*-
"""
脚本执行之前：
    1，退出登录
    2，清空所有课程
    3，清空所有考试
脚本执行结束，恢复到最开始的状态
"""
from framework.logger import Logger
from framework.HTMLTestRunner import HTMLTestRunner
import unittest
import time
import os

logger = Logger('ClassBox').logger

report_path = os.path.abspath('.') + '/test_reports/'

# 获取系统当前时间
now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))

# 设置报告名称格式
HtmlFile = report_path + now + "HTMLtemplate.html"
fp = open(HtmlFile, "wb")

# 构建suite


if __name__ == '__main__':
    suite = unittest.TestLoader().discover(os.path.abspath('.') + '/testsuits')


    # 初始化一个HTMLTestRunner实例对象，用来生成报告

    logger.info('课程格子app测试开始')
    runner = HTMLTestRunner(stream=fp, title=u"课程格子项目测试报告", description=u"测试app的安装和卸载", verbosity=2)
    # print(suite)
    # 开始执行测试套件
    runner.run(suite)
    logger.info('app测试结束')
    logger.info("测试报告已存入到'/test_reports'中")
    fp.close()