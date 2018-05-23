# -*- coding:utf-8 -*-
'''
本测试脚本实现了app的自动化安装和卸载
    1，测试安装（已有先卸载，再安装）
    2，测试app启动，然后进入登录页面
'''

import unittest
import logging
import time
from objects.app_install import AppInstall
from config.desired_caps import uri, desired_caps

logger = logging.getLogger('ClassBox')


@unittest.skip('')
class TestAppInstallAndRemove(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.debug("<<<<<<<<<<<<<1，安装app测试正式开始>>>>>>>>>>>>")
        cls.driver = AppInstall(uri, desired_caps)

    # 测试app安装和卸载
    @AppInstall.get_shot
    def test_01_app_install(self):
        if not self.driver.is_app_installed(desired_caps['appPackage']):
            logger.info("01, app尚未安装，正在执行安装app")
            self.driver.install_app()
            if self.driver.is_app_installed(desired_caps['appPackage']):
                logger.info("  app已安装成功")
            else:
                logger.info("  app安装失败")
        else:
            logger.info("  app已经存在，先卸载app")
            self.driver.remove_app(desired_caps['appPackage'])
            logger.info("  app卸载完成，正在安装app")
            self.driver.install_app(desired_caps['app'])
            if self.driver.is_app_installed(desired_caps['appPackage']):
                logger.info("  app已安装成功")
            else:
                logger.info("  app安装失败")
        time.sleep(5)
        self.assertTrue(self.driver.is_app_installed(desired_caps['appPackage']))

    # 测试app首次启动成功，并测试guide 页面
    @AppInstall.get_shot
    def test_02_guide_page(self):
        logger.info("02, 正在启动app")
        self.driver.launch_app()
        time.sleep(5)
        title = self.driver.find_title()
        self.driver.swipe_left(2)
        self.assertEqual("掌上校园", title)

    @classmethod
    def tearDownClass(cls):
        logger.info("    <<<<<<<<<<<<<<<<<安装、删除测试完成>>>>>>>>>>>>>>>>>>>")
        cls.driver.quit()