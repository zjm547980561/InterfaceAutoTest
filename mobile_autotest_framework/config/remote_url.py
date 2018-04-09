# -*- coding:utf-8 -*-
from appium import webdriver
from . import desired_caps

driver = webdriver.Remote(desired_caps.uri, desired_caps.desired_caps)