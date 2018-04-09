# -*- coding:utf-8 -*-
import unittest
from framework.logger import Logger
from config.desired_caps import desired_caps
from framework.driver import driver

logger = Logger('TestAppInstallAndRemove').get_logger()


class TestAppInstallAndRemove(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = driver

    def test_app_install(self):
        self.driver.install_app(desired_caps['app'])
        self.assertEqual(True, self.driver.is_app_installed(desired_caps['appPackage']))

    def test_app_remove(self):
        self.driver.remove_app(desired_caps['appPackage'])
        self.assertEqual(False, self.driver.is_app_installed(desired_caps['appPackage']))

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()