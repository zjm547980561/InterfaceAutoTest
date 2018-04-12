# -*- coding:utf-8 -*-



# class TestAppInstallAndRemove(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     cls.driver = driver
    #
    # def test_app_install(self):
    #     self.driver.install_app(desired_caps['app'])
    #     self.assertEqual(True, self.driver.is_app_installed(desired_caps['appPackage']))
    #
    # def test_guide_page(self):
    #     self.driver.launch_app()
    #     self.driver.swipe_left(5)
    #     self.driver.find_element(Guidepage.confirm).click()
    #     time.sleep(1)
    #     self.assertIsNotNone(self.driver.find_element(LogIn.phone))
    #
    # @classmethod
    # def tearDownClass(cls):
    #     cls.driver.quit()