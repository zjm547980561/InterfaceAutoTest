# -*- coding:utf-8 -*-

import logging
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver import Remote
from selenium.common.exceptions import NoSuchElementException
from functools import wraps

logger = logging.getLogger('ClassBox')


class Base(Remote):
    def quick_clear(self, el):
        logger.info("   定位快速清空按钮的位置")
        a = self.location_x(el) + self.width(el) - 2
        b = self.location_y(el) + self.height(el) / 2
        logger.info("   点击快速清空按钮")
        self.tap([(a, b)])

    def width(self, el):
        logger.info("   获取元素的宽度")
        return self.find_element_by_id(el).size['width']

    def height(self, el):
        logger.info("   获取元素的高度")
        return self.find_element_by_id(el).size['height']

    def location_x(self, el):
        logger.info("   获取元素的X坐标")
        return self.find_element_by_id(el).location['x']

    def location_y(self, el):
        logger.info("   获取元素的Y坐标")
        return self.find_element_by_id(el).location['y']

    # 定位元素是否存在
    def element_exist(self, ids):
        try:
            time.sleep(2)
            logger.info("   获取元素信息")
            self.find_element_by_id(ids)
            return True
        except NoSuchElementException:
            logger.debug("    没有此元素")
            return False
        else:
            logger.error("   无法获取元素信息, 错误原因：%s %s" % (e.__class__, e))
            return False

    # 元素的个数
    def number_of_elements(self, ids):
        if self.element_exist(ids):
            logger.info("    元素存在，个数为 %d" % len(self.find_elements_by_id(ids)))
            return len(self.find_elements_by_id(ids))
        else:
            logger.info("    元素不存在")
            return 0

    # 登录成功
    def loggin_success(self, account, passwd):
        logger.info("    输入手机号 %s" %account)
        self.send_data_to_element('mobile_ex', account)
        time.sleep(1)
        logger.info("    输入密码 %s" % passwd)
        self.send_data_to_element('password_ex', passwd)
        time.sleep(1)
        self.click_btn('confirm_tx')
        time.sleep(5)

    # 切换到"我的"页面
    def home_page(self):
        logger.info("    切换到'首页'")
        self.find_elements_by_xpath('//android.widget.FrameLayout[@resource-id="fm.jihua.kecheng:id/messages"]')[0].click()

    # 切换到"首页"页面
    def course_page(self):
        logger.info("    切换到'课表'页")
        self.find_elements_by_xpath('//android.widget.FrameLayout[@resource-id="fm.jihua.kecheng:id/messages"]')[1].click()

    # 切换到"我的"页面
    def my_page(self):
        logger.info("    切换到'我的'页")
        self.find_elements_by_xpath('//android.widget.FrameLayout[@resource-id="fm.jihua.kecheng:id/messages"]')[2].click()

    # 退出登录
    def logout(self):
        logger.info("    正在退出登录")
        time.sleep(1)
        self.my_page()
        time.sleep(1)
        self.click_btn('setting_iv')
        time.sleep(1)
        self.click_btn('logout')
        logger.info("    退出登录成功")
        time.sleep(5)

    def get_window_size_width(self):
        return self.get_window_size()['width']

    def get_window_size_height(self):
        return self.get_window_size()['height']

    #向左滑动
    def swipe_left(self, num):
        width = self.get_window_size_width()
        height = self.get_window_size_height()
        for i in range(num):
            self.swipe(width * 0.85, height * 0.5, width * 0.15, height * 0.5, 2000)
            logger.info("    向左滑动 第 %d 次" % (i+1))
            time.sleep(1)
        time.sleep(1)
        self.click_btn('confirm')

    # 向上滑动
    def swipe_up(self, num):
        width = self.get_window_size_width()
        height = self.get_window_size_height()
        for i in range(num):
            self.swipe(width * 0.5, height * 0.85, width * 0.5, height * 0.15, 2000)
            logger.info("    向上滑动 第 %d 次" % (i + 1))
            time.sleep(1)

    # 向右滑动
    def swipe_right(self, num):
        width = self.get_window_size_width()
        height = self.get_window_size_height()
        for i in range(num):
            self.swipe(width * 0.25, height * 0.5, width * 0.75, height * 0.5, 2000)
            logger.info("    向右滑动 第 %d 次" % (i + 1))

    # 定位toast信息
    def find_toast(self, message, el):
        toast_loc = ("xpath", ".//*[contains(@text,'%s')]" % message)
        time.sleep(1)
        logger.info("    获取提示信息")
        logger.info("    点击'确认'按钮 或者 '获取验证码'按钮 或者 '保存'按钮")
        self.click_btn(el)
        try:
            element = WebDriverWait(self, 10, 0.1).until(
                EC.presence_of_element_located(toast_loc))
            logger.info("    获取到的toast消息为：%s" % element.text)
            return True
        except Exception as e:

            logger.error('找不到toast消息：%s, error message: %s' % (message, e))
            time.sleep(2)
            # self.save_screenshot(filename)
            raise e

    # 装饰器
    @staticmethod
    def get_shot(func):
        @wraps(func)
        def dec(*args):
            try:
                func(*args)
            except AssertionError as e:
                logger.error(e)
                raise AssertionError
            except Exception as e:
                logger.error(e)
                raise Exception
        return dec

    # 用来测试登录不成功的方法
    def login(self, element, phone='', passwd='', success=False):
        time.sleep(1)
        logger.info("    输入手机号 %s" % phone)
        self.send_data_to_element(element['phone'], phone)
        time.sleep(1)
        logger.info("    输入密码 %s" % passwd)
        self.send_data_to_element(element['passwd'], passwd)
        time.sleep(1)
        if success:
            logger.info("    点击登录成功")
            self.click_btn('confirm_tx')
            time.sleep(5)

    # 发送数据
    def send_data_to_element(self, element, args):
        time.sleep(1)
        self.find_element_by_id(element).clear().send_keys(args)

    def send_data_to_elements(self, element, index, args):
        self.find_elements_by_id(element)[index].clear().send_keys(args)

    # 清空数据
    def clear_data(self, element):
        time.sleep(2)
        self.find_element_by_id(element).clear()

    # 点击按钮
    def click_btn(self, element):
        time.sleep(1)
        self.find_element_by_id(element).click()

    # 定位到多个按钮会，选择点击
    def click_btns(self, elements, idx):
        time.sleep(1)
        self.find_elements_by_id(elements)[idx].click()

    # 获取元素的大小
    def get_element_size(self, el):
        a = self.find_element_by_id(el).size
        logger.info("    获取元素的大小为： %s" % a)
        return a

    # 获取元素的内容
    def get_text(self, el):
        a = self.find_element_by_id(el).text
        logger.info("    获取元素的内容为：%s" % a)
        return a
