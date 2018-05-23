# -*- coding:utf-8 -*-
from framework.base import Base
from config.week_time import time_to_school, degree
import time
import logging


my_profile_toast = {
    'empty_name': u'昵称不能为空',
    'length_over_ten': u'不能超过10个字'
}

el = {
    'phone': 'mobile_ex',
    'passwd': 'password_ex',
    'confirm_btn': 'right_layout',
    'major': 'profession_tx',
    'search': 'search_ex',
    'name': 'name',
    'school': 'school_tx',
    'school_item': 'item'
}
data = {
    'phone': '15201418408',
    'passwd': '123456',
}
logger = logging.getLogger('ClassBox')


class MyProfile(Base):
    def click_name(self):
        time.sleep(2)
        logger.info("    点击昵称按钮")
        self.click_btn('alias_tx')
        time.sleep(2)

    def edit_name(self, name='test'):
        time.sleep(2)
        logger.info("    修改昵称为：%s" % name)
        self.send_data_to_element('alias_edit', name)
        time.sleep(2)

    def save(self):
        time.sleep(2)
        logger.info("    点击保存按钮")
        self.click_btn('right_layout')
        time.sleep(5)

    def name_value(self):
        time.sleep(2)
        a = self.find_element_by_id('alias_tx').text
        logger.info("    获取到的昵称为 %s" % a)
        return a

    def click_gender(self):
        time.sleep(2)
        logger.info("    点击性别按钮")
        self.click_btn('sex_tx')
        time.sleep(2)

    def modify_gender_male(self):
        time.sleep(2)
        logger.info("    修改性别为男")
        self.find_elements_by_class_name("android.widget.TextView")[2].click()
        time.sleep(2)

    def modify_gender_female(self):
        time.sleep(2)
        logger.info("    修改性别为女")
        self.find_elements_by_class_name("android.widget.TextView")[1].click()
        time.sleep(2)

    def gender_value(self):
        time.sleep(2)
        a = self.find_element_by_id('sex_tx').text
        logger.info("    获取性别：%s" % a)
        return a

    def click_birth(self):
        time.sleep(2)
        logger.info("    点击生日按钮")
        self.click_btn('birthday_layout')
        time.sleep(2)
        logger.info("    点击确定")
        self.find_elements_by_class_name("android.widget.TextView")[1].click()
        time.sleep(2)

    def click_birth_cancel(self):
        time.sleep(2)
        logger.info("    点击生日按钮")
        self.click_btn('birthday_layout')
        time.sleep(2)
        logger.info("    点击取消")
        self.find_elements_by_class_name("android.widget.TextView")[0].click()
        time.sleep(2)

    def click_time_to_school(self, name):
        time.sleep(2)
        logger.info("    点击入学时间按钮")
        self.click_btn('school_time_tx')
        time.sleep(2)
        logger.info("    选择入学时间为：%s 年" %name)
        self.click_btns('item', time_to_school[name])
        time.sleep(2)

    def time_to_value(self):
        time.sleep(2)
        a = self.find_element_by_id('school_time_tx').text
        logger.info("    获取入学时间：%s" % a)
        return a

    def click_degree(self):
        time.sleep(2)
        logger.info("    点击学位按钮")
        self.click_btn('degree_tx')
        time.sleep(2)

    def degree_alter(self, name="大学生"):
        time.sleep(2)
        logger.info("    选择学位：%s" % name)
        self.click_btns('education', degree[name])
        time.sleep(2)

    def degree_value(self):
        time.sleep(2)
        a = self.find_element_by_id('degree_tx').text
        logger.info("    获取学位 %s" % a)
        return a

    def birth_value(self):
        time.sleep(2)
        a = self.find_element_by_id('birthday_tx').text
        logger.info("    获取生日日期 %s" % a)
        return a

    def major_value(self):
        time.sleep(2)
        a = self.find_element_by_id(el['major']).text
        logger.info("    获取专业信息 %s" % a)
        return a

    def click_major(self):
        time.sleep(2)
        logger.info('   点击专业按钮')
        self.click_btn(el['major'])
        time.sleep(2)

    def click_school(self):
        time.sleep(2)
        logger.info('   点击就读院校')
        self.click_btn(el['school'])
        time.sleep(2)

    def search_major(self, item):
        time.sleep(2)
        logger.info('   搜索专业：%s' %item)
        self.send_data_to_element(el['search'], item)
        time.sleep(2)

    def school_value(self):
        time.sleep(2)
        return self.get_text(el['school'])

    def back_btn(self):
        logger.info("    点击返回按钮")
        self.click_btn('iv_left')
        time.sleep(2)