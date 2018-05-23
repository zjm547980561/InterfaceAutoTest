# -*- coding:utf-8 -*-
'''
添加考试，手动输入和直接添加
'''
from framework.base import Base
import time
import logging
logger = logging.getLogger("ClassBox")

toast_msg = {
    "update": u'更新成功',
    "delete": u'删除成功',
    "empty_name": u'考试名称不能为空',
    "empty_time": u'时间不能为空',
}

el = {
    'phone': 'mobile_ex',
    'passwd': 'password_ex',
    'confirm': 'confirm',
    'confirm_btn': 'right_layout',
    'confirm_tx': 'confirm_tx'
}
data = {
    'phone': '15201418408',
    'passwd': '123456',
}

class AddTests(Base):
    # 进入考试页面
    def enter_test_page(self):
        time.sleep(1)
        logger.info("    点击课表页的'考试'按钮")
        self.click_btn('left_parent')

    # 进入备考tab
    def prepare_test(self):
        time.sleep(1)
        logger.info("    进入'备考'tab")
        self.click_btns('name', 0)

    # 进入完成考试tab
    def finished_test(self):
        time.sleep(1)
        logger.info("    进入'考试'tab")
        self.click_btns('name', 1)

    # 没有考试时，备考tab中有添加考试按钮
    def add_test_btn(self):
        time.sleep(1)
        logger.info("    没有考试时，备考tab中有'添加考试'按钮")
        self.click_btn('add_exam_tx')

    # 右上角的+号按钮
    def add_test_symbol(self):
        time.sleep(1)
        logger.info("    点击课表页的添加考试按钮即 '+' ")
        self.click_btn('right_parent')

    # 关闭添加考试页面
    def close_add(self):
        time.sleep(1)
        logger.info("    关闭添加考试页面")
        self.click_btn('left_layout')

    # 进入课程考试tab
    def course_test(self):
        time.sleep(1)
        logger.info("    进入科目考试tab")
        self.click_btns('name', 0)

    # 进入统一考试tab
    def universe_test(self):
        time.sleep(1)
        logger.info("    进入统一考试tab")
        self.click_btns('name', 1)

    # 进入自定义考试tab
    def custom_test(self):
        time.sleep(1)
        logger.info("    进入自定义考试tab")
        self.click_btns('name', 2)

    # 点击添加 考试按钮
    def add_test(self):
        time.sleep(1)
        logger.info("    点击需要添加的科目")
        self.click_btns('add_icon', 0)

    # 保存添加的考试
    def save_test(self):
        time.sleep(1)
        logger.info("    保存添加的考试")
        self.click_btn('confirm')

    # 输入自定义考试-名称
    def test_name(self, name="test"):
        time.sleep(1)
        logger.info("    输入考试名称：%s" % name)
        self.send_data_to_element('exam_name', name)

    # 输入自定义考试-位置
    def test_location(self):
        time.sleep(1)
        logger.info("    输入考试地点：123")
        self.send_data_to_element('exam_address', '123')

    # 输入自定义考试-日期
    def define_test_time_date(self):
        logger.info("    点击设置考试时间-日期")
        self.click_btn('exam_time')
        time.sleep(2)
        for i in range(1):
            a = self.get_window_size()['height'] - self.find_element_by_id('day').size['height'] / 5 * 1.5
            b = self.get_window_size()['width'] / 4
            self.tap([(b, a)], 10)
            time.sleep(1)

    def current_hour(self):
        temp = time.asctime(time.localtime(time.time())).split()[3].split(':')[0]
        return int(temp)

    # 输入自定义考试-小时
    def define_test_time_hour(self):
        logger.info("    点击设置考试时间-小时")
        self.click_btn('exam_time')
        time.sleep(2)
        for i in range(self.current_hour()):
            a = self.get_window_size()['height'] - self.find_element_by_id('hour').size['height'] / 5 * 1.5
            b = self.get_window_size()['width'] / 4 * 2.5
            self.tap([(b, a)], 10)
            time.sleep(1)

    # 输入自定义考试-分钟
    def define_test_time_minute(self):
        logger.info("    点击设置考试时间-分钟")
        self.click_btn('exam_time')
        time.sleep(2)
        for i in range(5):
            a = self.get_window_size()['height'] - self.find_element_by_id('min').size['height'] / 5 * 1.5
            b = self.get_window_size()['width'] / 4 * 3.5
            self.tap([(b, a)], 10)
            time.sleep(1)

    # 测试没有结束的考试时，没有查询成绩按钮
    def grade_query_exist(self):
        logger.info("    进入已完成考试tab")
        self.finished_test()
        time.sleep(1)
        if self.element_exist('score_check'):
            return True
        else:
            return False

    def edit_exam(self):
        time.sleep(1)
        logger.info("    点击修改考试按钮")
        self.click_btn('right_layout')

    # 测试modify exam
    def modify_exam(self):
        time.sleep(1)
        logger.info("    点击要修改的考试条目")
        self.click_btn('item_layout')
        self.edit_exam()
        logger.info("    修改考试时间，使此考试变成已完成状态")
        self.click_btn('exam_time_tx')
        a = self.get_window_size()['height'] - self.find_element_by_id('hour').size['height'] / 2
        b = self.get_window_size()['width'] / 4
        self.tap([(b, a)], 10)

    # 测试删除考试
    def delete_exam(self):
        time.sleep(1)
        logger.info("    点击要修改的考试条目")
        self.click_btn('item_layout')
        self.edit_exam()



