# -*- coding:utf-8 -*-
'''
本脚本主要测试添加考试
1，有考试
2，没考试
3，添加考试
4，删除考试
5，修改考试
...

'''

import unittest
import logging
from objects.add_tests import AddTests, toast_msg, el, data
import time
from config.desired_caps import uri, desired_caps
logger = logging.getLogger('ClassBox')


@unittest.skip('')
class TestAddTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.info('<<<<<<<<<<<<<<<<<<<<7，添加考试测试现在开始>>>>>>>>>>>>>>>>>>>>>')
        cls.driver = AddTests(uri, desired_caps)
        try:
            cls.driver.launch_app()
            logger.info("    正在启动app")
            time.sleep(5)
            cls.driver.login(el, data['phone'], data['passwd'], success=True)
            time.sleep(1)
            cls.driver.course_page()
            cls.driver.enter_test_page()

        except Exception as e:
            logger.error(e)
            logger.info("    app启动失败")
            cls.driver.quit()

    # 测试没有考试时，备考中显示添加考试按钮
    @AddTests.get_shot
    def test_01_no_exam(self):
        logger.info('01, 测试没有考试时，备考中显示添加考试按钮')
        self.driver.prepare_test()
        a = self.driver.element_exist('add_exam_tx')
        self.assertEqual(True, a)

    # 测试点击"添加考试"按钮进入添加页面
    @AddTests.get_shot
    def test_02_1_enter_add_exam_page(self):
        logger.info('02-1, 测试点击"添加考试"按钮进入添加页面')
        self.driver.add_test_btn()
        self.driver.close_add()
        self.assertTrue(True)

    # 测试点击加号进入添加考试页面
    @AddTests.get_shot
    def test_02_2_enter_add_exam_page(self):
        logger.info('02-2, 测试点击加号进入添加考试页面')
        self.driver.add_test_symbol()
        a = self.driver.element_exist('add_icon')
        self.assertEqual(False, a)

    # 测试添加统一考试
    @AddTests.get_shot
    def test_03_add_universe_exam(self):
        logger.info('03, 测试添加统一考试')
        self.driver.universe_test()
        self.driver.add_test()
        self.driver.save_test()
        self.assertTrue(True)

    # 测试添加考试名称为空
    def test_04_empty_name(self):
        logger.info('04, 测试添加考试名称为空')
        self.driver.custom_test()
        a = self.driver.find_toast(toast_msg["empty_name"], el['confirm'])
        self.assertTrue(a)

    # 测试添加考试时间为空
    @AddTests.get_shot
    def test_05_empty_time(self):
        logger.info('05, 试添加考试时间为空')
        self.driver.test_name()
        a = self.driver.find_toast(toast_msg["empty_time"], el['confirm'])
        self.assertTrue(a)

    # 测试自定义添加考试成功
    @AddTests.get_shot
    def test_06_add_custom_exam(self):
        logger.info('06, 测试自定义添加考试成功')
        self.driver.test_location()
        self.driver.define_test_time_date()
        self.driver.define_test_time_hour()
        self.driver.define_test_time_minute()
        self.driver.save_test()
        a = self.driver.number_of_elements('item_layout')
        self.assertEqual(2, a)

    # 测试有考试时，备考tab不显示添加考试的按钮
    @AddTests.get_shot
    def test_07_add_button_not_exist(self):
        logger.info('07, 测试有考试时，备考tab不显示添加考试的按钮')
        self.driver.prepare_test()
        a = self.driver.element_exist('add_exam_tx')
        self.assertEqual(False, a)

    # 测试没有完成的考试时，没有成绩查询按钮
    @AddTests.get_shot
    def test_08_grade_query_not_exist(self):
        logger.info('08, 测试没有完成的考试时，没有成绩查询按钮')
        a = self.driver.grade_query_exist()
        self.driver.prepare_test()
        self.assertEqual(a, False)

    # 测试修改考试，使之变成完成状态
    @AddTests.get_shot
    def test_09_modify_exam(self):
        logger.info('09, 测试修改考试，使之变成完成状态')
        self.driver.modify_exam()
        a = self.driver.find_toast(toast_msg["update"], el['confirm_btn'])
        self.assertTrue(a)

    # 测试修改考试，使之变成完成状态后，备考tab中只有一个考试条目
    @AddTests.get_shot
    def test_10_ckeck_prepare_exam(self):
        logger.info('10, 测试修改考试，使之变成完成状态后，备考tab中只有一个考试条目')
        a = self.driver.number_of_elements('item_layout')
        self.assertEqual(1, a)

    # 测试修改考试，使之变成完成状态后，完成tab中有一个考试条目
    @AddTests.get_shot
    def test_11_ckeck_finished_exam(self):
        logger.info('11, 测试修改考试，使之变成完成状态后，完成tab中有一个考试条目')
        self.driver.finished_test()
        a = self.driver.number_of_elements('item_layout')
        self.assertEqual(1, a)

    # 测试修改考试，使之变成完成状态后，完成tab中有成绩查询
    @AddTests.get_shot
    def test_12_ckeck_grade_query_btn(self):
        logger.info('12, 测试修改考试，使之变成完成状态后，完成tab中有成绩查询')
        a = self.driver.grade_query_exist()
        self.driver.prepare_test()
        self.assertEqual(a, True)

    # 测试删除备考中考试
    @AddTests.get_shot
    def test_13_delete_prepare_exam(self):
        logger.info('13, 测试删除备考中考试')
        self.driver.delete_exam()
        a = self.driver.find_toast(toast_msg["delete"], el['confirm_tx'])
        self.assertTrue(a)

    # 测试核实删除考试
    @AddTests.get_shot
    def test_14_ckeck_delete_prepare_exam(self):
        logger.info('14, 测试核实删除考试')
        a = self.driver.element_exist('item_layout')
        self.assertEqual(False, a)

    # 测试删除finished考试
    @AddTests.get_shot
    def test_15_ckeck_delete_prepare_exam(self):
        logger.info('15, 测试删除finished考试')
        self.driver.finished_test()
        self.driver.delete_exam()
        a = self.driver.find_toast(toast_msg["delete"], el['confirm_tx'])
        self.assertTrue(a)

    # 测试核实删除finished考试
    @AddTests.get_shot
    def test_16_ckeck_delete_finished_exam(self):
        logger.info('16, 测试核实删除finished考试')
        a = self.driver.element_exist('item_layout')
        self.assertEqual(False, a)

    # 测试没有考试时，备考中显示添加考试按钮
    @AddTests.get_shot
    def test_17_no_exam(self):
        logger.info('17, 测试没有考试时，备考中显示添加考试按钮')
        self.driver.prepare_test()
        a = self.driver.element_exist('add_exam_tx')
        self.assertEqual(True, a)

    @classmethod
    def tearDownClass(cls):
        logger.info('<<<<<<<<<<<<<<<<<<<添加考试测试已结束>>>>>>>>>>>>>>>>>>>')
        cls.driver.logout()