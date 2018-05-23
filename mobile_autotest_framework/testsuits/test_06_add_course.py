# -*- coding:utf-8 -*-

"""
测试添加课程
1，课程名为空
2，手动添加课程成功
3，删除课程
4，自动添加课程为空
"""

import unittest
import logging
import time
from objects.add_course import AddCourse, toast_msg, el, data
from config.desired_caps import desired_caps, uri
logger = logging.getLogger('ClassBox')


@unittest.skip('')
class TestAddCourse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.debug("<<<<<<<<<<<<<6，添加课程功能测试正式开始>>>>>>>>>>>>")
        cls.driver = AddCourse(command_executor=uri, desired_capabilities=desired_caps)
        try:
            logger.info("    正在启动app")
            cls.driver.launch_app()
            time.sleep(5)
            cls.driver.login(el, data['phone'], data['passwd'], success=True)
            time.sleep(1)
            logger.info("    进入'课表'页")
            cls.driver.course_page()
            cls.num = cls.driver.acquire_current_week() - 1
        except Exception as e:
            logger.error(e)
            logger.info("    app启动失败")
            cls.driver.quit()

    @AddCourse.get_shot
    def test_01_none_course(self):
        logger.info('01，测试课表没有课时，课表页有添课按钮')
        a = self.driver.element_exist('add_course')
        self.assertEqual(True, a)

    @AddCourse.get_shot
    def test_02_enter_add_course_page(self):
        logger.info('02，测试点击添课按钮进入添课页面')
        self.driver.click_btn('add_course')
        time.sleep(1)
        a = self.driver.current_activity
        self.driver.click_btn('left_layout')
        self.assertEqual(a, '.ui.course.AddCourseActivity')

    @AddCourse.get_shot
    def test_03_empty_course(self):
        logger.info('03，测试手动添加课程，课程名为空')
        self.driver.access_to_add()
        self.driver.click_add_course()
        self.driver.click_free_add_course()
        self.driver.click_add_course_with_hand()
        self.driver.empty_course()
        a = self.driver.find_toast(toast_msg, el['confirm'])
        self.assertTrue(a)

    @AddCourse.get_shot
    def test_04_manual_add_success(self):
        logger.info('04，测试手动添加课程成功')
        self.driver.type_course_name('test')
        self.driver.type_teacher_name('tester')
        self.driver.type_location_name('123')
        self.driver.add_week(index=self.num)
        self.driver.add_week_time()
        self.driver.add_start_time()
        self.driver.tap_empty()
        self.driver.save_course()
        time.sleep(2)
        self.driver.back_to_curriculum()
        a = self.driver.verify_add()
        self.assertTrue(a)

    @AddCourse.get_shot
    def test_05_add_course_btn_disappear(self):
        logger.info('05，测试课表有课后，课表页的添课按钮消失')
        a = self.driver.element_exist("add_course")
        self.assertEqual(a, False)

    @AddCourse.get_shot
    def test_06_hide_course(self):
        logger.info('06，测试隐藏非本周课程')
        self.driver.access_to_add()
        self.driver.enter_course_setting()
        self.driver.hide_course_btn()
        self.driver.hide_course()
        self.driver.back_to_class_page()
        a = self.driver.verify_add()
        self.assertEqual(a, False)

    @AddCourse.get_shot
    def test_07_show_course(self):
        logger.info('07，测试显示非本周课程')
        self.driver.access_to_add()
        self.driver.enter_course_setting()
        self.driver.hide_course_btn()
        self.driver.show_course()
        self.driver.back_to_class_page()
        a = self.driver.verify_add()
        self.assertEqual(a, True)

    @AddCourse.get_shot
    def test_08_delete_course(self):
        logger.info('08，测试删除课程')
        self.driver.delete_course()
        a = self.driver.verify_add()
        self.assertFalse(a)

    # @AddCourse.get_shot
    @unittest.skip('')
    def test_09_auto_add_success(self):
        logger.info('09，测试自动导入课程')
        self.driver.auto_add_course()
        a = self.driver.verify_add()
        self.assertTrue(a)

    @AddCourse.get_shot
    def test_10_enter_class_setting_page(self):
        logger.info('10，测试进入课表设置页面')
        time.sleep(1)
        self.driver.setting_class()
        time.sleep(1)
        a = self.driver.current_activity
        self.assertEqual(a, '.ui.setting.ClassTimeActivity')

    @AddCourse.get_shot
    def test_11_set_number_of_class(self):
        logger.info('11，测试设置课程节数')
        a = self.driver.everyday_class()
        self.driver.alter_number_of_class()
        b = self.driver.number_of_class()
        self.assertEqual(1, (b - a))

    @AddCourse.get_shot
    def test_12_modify_current_week(self):
        logger.info('12, 测试修改当前周')
        a = self.driver.acquire_current_week()
        logger.info("   当前周数为 %d" % a)
        self.driver.modify_current_week_to_next_week()
        b = self.driver.acquire_current_week()
        logger.info("   修改后，当前周数变成 %d" % b)
        self.assertEqual(1, (b-a))

    @AddCourse.get_shot
    def test_13_modify_back(self):
        logger.info('13, 恢复环境')
        self.driver.back_to_current_week()
        a = self.driver.acquire_current_week()
        logger.info("   当前周数为 %d" % a)
        self.assertTrue(True)

    @classmethod
    def tearDownClass(cls):
        logger.info("<<<<<<<<<<<<<<<<<<<添加课程功能测试完毕>>>>>>>>>>>>>>>>>>>>>")
        cls.driver.logout()
        cls.driver.quit()