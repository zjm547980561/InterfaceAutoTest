# -*- coding:utf-8 -*-
desired_caps = dict()
desired_caps['automationName'] = 'UiAutomator2'
desired_caps['platformName'] = 'Android'
# oppo r9s
# desired_caps['platformVersion'] = '6.0.1'
# desired_caps['deviceName'] = 'd331cc56'
# oppo r11s
desired_caps['platformVersion'] = '7.1.1'
desired_caps['deviceName'] = '702d6a85'
desired_caps['appPackage'] = 'fm.jihua.kecheng'
desired_caps['resetKeyboard'] = True
# desired_caps['unicodeKeyboard'] = True
# desired_caps['app'] = '/Users/edz/Desktop/kecheng-production-release.apk_10.0.8.apk'
desired_caps['noReset'] = True
desired_caps['newCommandTimeout'] = 3600
desired_caps['appActivity'] = '.ui.BaseSplashActivity'

uri = 'http://127.0.0.1:4723/wd/hub'