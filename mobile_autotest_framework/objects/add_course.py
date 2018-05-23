# -*- coding:utf-8 -*-
'''
手动添加课程，教务系统自动导入
'''
from config.week_time import week, start_time, week_btn
import time
from framework.base import Base
import logging
from framework.configparse import all_account

toast_msg = u'课程名不能为空！'
logger = logging.getLogger('ClassBox')
el = {
    'phone': 'mobile_ex',
    'passwd': 'password_ex',
    'confirm': 'right_layout'
}
data = {
    'phone': '15201418408',
    'passwd': '123456',
}


class AddCourse(Base):
    # 输入课程名
    def type_course_name(self, name="test"):
        time.sleep(1)
        logger.info("    输入课程名称 %s" % name)
        self.send_data_to_element('course_name', name)

    # 输入老师名
    def type_teacher_name(self, name=None):
        time.sleep(1)
        logger.info("    输入老师名称 %s" % name)
        self.send_data_to_element('teacher_name', name)

    # 输入教室名
    def type_location_name(self, name=None):
        time.sleep(1)
        logger.info("    输入上课地点 %s" % name)
        self.send_data_to_element('room', name)

    # 点击关闭选择上课时间下拉框
    def tap_empty(self):
        time.sleep(1)
        logger.info("    点击空白区域")
        self.tap([(200, 200)])

    # 测试课程名为空
    def empty_course(self):
        time.sleep(1)
        self.save_course()

    # 教务系统账号
    def type_school_account(self, name=None):
        time.sleep(1)
        logger.info("    输入教务系统账号：%s" % name)
        self.send_data_to_elements('et_param', 0, name)

    # 教务导入课程按钮
    def click_submit(self):
        time.sleep(1)
        logger.info("    点击导入按钮")
        self.click_btn('import_course')

    # 教务系统密码
    def type_school_passwd(self, name=None):
        time.sleep(1)
        logger.info("    输入教务系统密码：%s" % name)
        self.send_data_to_elements('et_param', 1, name)

    # 自动添加课程
    def auto_add_course(self):
        self.access_to_add()
        self.click_add_course()
        self.click_school_add_course()
        self.type_school_account(all_account[2])
        self.type_school_passwd(all_account[3])
        self.click_submit()

    # 点击手动添加按钮, 手动添加课程
    def click_add_course_with_hand(self):
        time.sleep(1)
        self.swipe_up(3)
        time.sleep(1)
        logger.info("    点击'手动添加课程'按钮")
        self.click_btn('add_course')

    def add_course_manual_success(self):
        self.type_course_name('test')
        self.type_teacher_name('tester')
        self.type_location_name('123')
        a = self.acquire_current_week()
        self.add_week(index=a)
        self.add_week_time()
        self.add_start_time()
        self.tap_empty()
        self.save_course()
        time.sleep(2)
        self.back_to_curriculum()

    # 选择上课周数
    def add_week(self, index=None, all_week=2):
        time.sleep(1)
        logger.info("    点击周数按钮")
        self.click_btn('week')
        if not all_week == 2:
            time.sleep(2)
            self.click_btn(week_btn[all_week])
            if index:
                time.sleep(2)
                self.click_btns('checkBox1', index)
            else:
                pass
        else:
            if index:
                time.sleep(2)
                self.click_btns('checkBox1', index)
            else:
                pass
        time.sleep(2)
        logger.info("    点击保存按钮")
        self.click_btn('btn_save')

    @staticmethod
    def week_to_num():
        time.sleep(1)
        temp = time.asctime(time.localtime(time.time())).split()[0]
        return week[temp]

    @staticmethod
    def time_to_num():
        time.sleep(1)
        temp = time.asctime(time.localtime(time.time())).split()[3].split(':')[0]
        return start_time[temp]

    # 选择添加的课程是星期几
    def add_week_time(self):
        time.sleep(1)
        logger.info("    点击上课时间按钮，选择上课是周几")

        self.click_btn("time")
        time.sleep(1)
        logger.info("   元素的大小是： %s" % self.find_element_by_id('weekday').size)
        time.sleep(2)
        for i in range(self.week_to_num()):
            a = self.get_window_size()['height'] - self.find_element_by_id('weekday').size['height'] / 5 * 1.5
            b = self.get_window_size()['width'] / 6
            self.tap([(b, a)])
            logger.info("   点击了 %d 次" % (i+1))
            time.sleep(1)

    # 选择添加上课的时间
    def add_start_time(self):
        time.sleep(1)
        logger.info("    添加上课具体节数")
        for i in range(self.time_to_num()):
            a = self.get_window_size()['height'] - self.find_element_by_id('start').size['height'] / 5 * 1.5
            b = self.get_window_size()['width'] / 6 * 3
            self.tap([(b, a)])
            logger.info("   点击了 %d 次" % (i+1))
            time.sleep(1)

    # 点击课表的'+'号按钮
    def access_to_add(self):
        time.sleep(1)
        logger.info("    点击上课")
        self.click_btn('right_parent')

    # 点击添课按钮
    def click_add_course(self):
        time.sleep(1)
        logger.info("    点击添加课程按钮")
        self.click_btn('add')

    # 点击自由添课按钮
    def click_free_add_course(self):
        time.sleep(1)
        logger.info("    点击自由添加课程tab")
        self.click_btns('name', 1)

    # 点击教务导入
    def click_school_add_course(self):
        time.sleep(1)
        logger.info("    点击教务导入tab")
        self.click_btns('name', 0)

    # 保存添加的课程
    def save_course(self):
        time.sleep(1)
        logger.info("    点击保存按钮")
        self.click_btn('right_layout')

    # 返回课表
    def back_to_curriculum(self):
        time.sleep(1)
        logger.info("    点击弹窗，返回到课表页")
        self.find_elements_by_class_name('android.widget.Button')[1].click()

    # 继续加课
    def add_course_again(self):
        time.sleep(1)
        logger.info("    点击弹窗，继续添加课程")
        self.find_elements_by_class_name('android.widget.Button')[0].click()

    # 找到添加的课程
    def delete_course(self):
        time.sleep(1)
        logger.info("    点击已存在的课程")
        self.find_element_by_xpath('//android.widget.FrameLayout[@resource-id="fm.jihua.kecheng:id/content"]/android.widget.TextView').click()
        time.sleep(1)
        logger.info("    点击删除按钮")
        self.click_btn('delete_course')

    # 验证是否添课成功
    def verify_add(self):
        time.sleep(2)
        num = len(self.find_elements_by_xpath('//android.widget.FrameLayout[@resource-id="fm.jihua.kecheng:id/content"]/android.widget.TextView'))
        logger.info('    课表中共有 %s 门课' % num)
        if num == 1:
            return True
        else:
            return False

    # 进入设置
    def setting_class(self):
        time.sleep(1)
        logger.info("    点击课表页中的时间设置")
        self.click_btn('section_time')

    # 设置每日课程节数
    def setting_classes(self):
        time.sleep(1)
        logger.info("    点击每日课程数量")
        self.click_btn('courses_everyday_layout')

    # 获取元素的位置
    def acquire_location(self):
        time.sleep(1)
        logger.info("    得到选择框位置")
        return self.find_element_by_id('loop').location

    # 计算要点击区域的X坐标
    def x_location(self):
        time.sleep(1)
        logger.info("    得到选择框的X坐标")
        return  (self.acquire_location()['x'] + self.get_element_size('loop')['width']) / 2

    # 计算要点击区域的Y坐标
    def y_location(self):
        time.sleep(1)
        logger.info("    得到选择框的Y坐标")
        return self.acquire_location()['y'] + self.get_element_size('loop')['height'] / 6 * 4

    # 点击要选择的课程节数区域
    def click_location(self):
        time.sleep(1)
        self.tap([(self.x_location(), self.y_location())])

    # 确认选择的课程节数
    def alter_number_of_class(self):
        self.setting_classes()
        self.click_location()
        self.click_btn('confirm')
        self.save_course()

    # 获取每日设置的课程节数
    def everyday_class(self):
        a = int(self.get_text('courses_everyday_tx').split('节')[0])
        logger.info("获取课表设置的课程节数，每天的课程节数设置为 %d" % a)
        return a

    # 课表上显示的课程节数
    def number_of_class(self):
        time.sleep(1)
        start_x = self.find_element_by_xpath('//android.widget.FrameLayout[@resource-id="fm.jihua.kecheng:id/container"]').location['x'] + \
                  (self.find_element_by_xpath('//android.widget.FrameLayout[@resource-id="fm.jihua.kecheng:id/container"]').size['width'] / 2)
        start_y = self.find_element_by_xpath('//android.widget.FrameLayout[@resource-id="fm.jihua.kecheng:id/container"]').location['y'] + \
                  (self.find_element_by_xpath('//android.widget.FrameLayout[@resource-id="fm.jihua.kecheng:id/container"]').size['height'] / 2)
        end_x = self.find_element_by_xpath('//android.widget.FrameLayout[@resource-id="fm.jihua.kecheng:id/container"]').location['x']
        end_y = self.find_element_by_xpath('//android.widget.FrameLayout[@resource-id="fm.jihua.kecheng:id/container"]').location['y']
        size_x = self.find_element_by_xpath('//android.widget.FrameLayout[@resource-id="fm.jihua.kecheng:id/container"]').size['width']
        size_y = self.find_element_by_xpath('//android.widget.FrameLayout[@resource-id="fm.jihua.kecheng:id/container"]').size['height']
        logger.info('    滑动的起点坐标为（%d %d）' % (start_x, start_y))
        logger.info('    滑动的终点坐标为（%d %d）' % (end_x, end_y))
        logger.info('    元素的大小（%d %d）' % (size_x, size_y))
        self.swipe(start_x, start_y, start_x, end_y, 1000)
        return int(self.find_elements_by_id('section_name').pop().text)

    # 获取当前周数

    def acquire_current_week(self):
        time.sleep(1)
        return int(self.get_text('center_text').split('周')[0].split('第')[1])

    # 获取当前学期
    def acquire_current_term(self):
        time.sleep(1)
        return self.get_text('sub_title')

    # 修改当前周数
    def modify_current_week_to_next_week(self):
        time.sleep(1)
        logger.info("    点击课表页面的第X周按钮")
        self.click_btn('text_layout')
        time.sleep(1)
        logger.info("    点击修改当前周按钮")
        self.click_btn('ll_set_current_week')
        x = self.get_window_size_width() / 2
        y = self.get_window_size_height() - self.find_element_by_id('loop').size['height'] / 5 * 1.5
        self.tap([(x,y)])
        logger.info("    点击确认按钮")
        self.click_btn('confirm')

    def back_to_current_week(self):
        time.sleep(2)
        logger.info("    点击课表页面的第X周按钮")

        self.click_btn('text_layout')
        time.sleep(1)
        logger.info("    点击修改当前周按钮")
        self.click_btn('ll_set_current_week')
        time.sleep(1)
        logger.info("   元素的大小是： %s" % self.find_element_by_id('loop').size)
        x = self.get_window_size_width() / 2
        y = self.get_window_size_height() - self.find_element_by_id('loop').size['height'] / 5 * 3.5
        self.tap([(x,y)])
        logger.info("    点击确认按钮")
        self.click_btn('confirm')

    # 进入课表设置页面
    def enter_course_setting(self):
        time.sleep(1)
        logger.info("    进入课表设置页面")
        self.click_btn('week_start_layout')

    # 点击非本周课程设置
    def hide_course_btn(self):
        time.sleep(1)
        logger.info("    点击非本周设置按钮")
        self.click_btn('hide_course_layout')

    # 隐藏非本周课程
    def hide_course(self):
        time.sleep(1)
        logger.info("    非本周设置选择隐藏")
        self.click_btn('hide')

    # 显示非本周课程
    def show_course(self):
        time.sleep(1)
        logger.info("    非本周设置选择显示")
        self.click_btn('show')

    # 返回到课表页
    def back_to_class_page(self):
        time.sleep(1)
        logger.info("    返回到'课表'页")
        self.click_btn('left_layout')







