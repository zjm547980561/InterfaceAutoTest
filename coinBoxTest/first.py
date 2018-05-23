# -*- coding:utf-8 -*-

from appium import webdriver
import time


desired_caps = dict()
desired_caps['automationName'] = 'Appium'
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0'
desired_caps['deviceName'] = 'samsung'
# install app
desired_caps['app'] = '/Users/edz/Desktop/kechenggezi_163.apk'
desired_caps['appPackage'] = 'fm.jihua.kecheng'
desired_caps['appActivity'] = '.ui.register.RegisterActivity'
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
user = '15201418408'
passwd = 'zJM123456'
time.sleep(2)
phone = driver.find_element_by_id('mobile_ex')
phone.send_keys(user)
time.sleep(2)
pa = driver.find_element_by_id('password_ex')
pa.send_keys(passwd)
time.sleep(2)
confirm = driver.find_element_by_id('confirm_tx')
confirm.click()

ico = driver.find_element_by_class_name('android.widget.ImageView')
print(ico)
