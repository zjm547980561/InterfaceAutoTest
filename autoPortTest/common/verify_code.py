from selenium import webdriver
import os
import random
import time
from selenium.common.exceptions import NoSuchElementException
import logging


path = os.path.abspath('.')
path = path + "/tools/chromedriver"
char = [chr(i) for i in range(97, 123)]
logger = logging.getLogger('coinBox')
flag = False


def create_email_pre():
    result = ''
    for i in range(4):
        dig = char[random.randint(0, 25)]
        st = str(random.randint(0, 100))
        result = result + dig + st
    return result


class Web(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=path)
        time.sleep(2)

    def open_http(self):
        logger.debug("打开：http://www.bccto.me/")
        self.driver.get("http://www.bccto.me/")

    @property
    def get_email(self):
        self.enter_mail()
        self.click_apply_email()
        mail = self.driver.find_element_by_id("showmail").text
        logger.debug("  获取邮箱全称：%s" % mail)
        return mail

    def click_apply_email(self):
        logger.debug("  点击申请邮箱按钮")
        self.driver.find_element_by_id("applyMail").click()
        time.sleep(2)

    def enter_mail(self):
        self.driver.find_element_by_id("mailuser").clear()
        time.sleep(2)
        email = create_email_pre()
        logger.debug("  输入要申请的邮箱前缀 %s" % email)
        self.driver.find_element_by_id("mailuser").send_keys(email)
        time.sleep(2)

    @property
    def get_code(self):
        if self.get_code_element:
            return self.get_code_element.split("是")[1]
        else:
            return None

    @property
    def get_new_code(self):
        if self.get_new_code_element:
            return self.get_new_code_element.split("是")[1]
        else:
            return None

    @property
    def get_code_element(self):
        c = 0
        global flag
        flag = False
        while True:
            try:
                text = self.driver.find_element_by_xpath("//*[@id='inbox']/tr[2]/td[3]").text
                return text
            except NoSuchElementException as e:
                logger.error(e)
                time.sleep(1)
                c += 1
                if c == 61:
                    flag = True
                    return None

    @property
    def get_new_code_element(self):
        c = 0
        global flag
        flag = False
        while True:
            try:
                text = self.driver.find_element_by_xpath("//*[@id='inbox']/tr[3]/td[3]").text
                return text
            except NoSuchElementException as e:
                logger.error(e)
                time.sleep(1)
                c += 1
                if c == 61:
                    flag = True
                    return None


# if __name__ == "__main__":
web = Web()
