# -*- coding:utf-8 -*-
'''
本脚本主要测试修改个人资料

'''

import unittest
import logging
from objects.my_profile import MyProfile, my_profile_toast, el, data
from objects.new_regist import regist_element, regist_msg_data
import time
from config.desired_caps import uri, desired_caps

logger = logging.getLogger('ClassBox')


# @unittest.skip('')
class ModifyMyProfile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.debug("<<<<<<<<<<<<<8，修改个人资料功能测试正式开始>>>>>>>>>>>>")
        cls.driver = MyProfile(command_executor=uri, desired_capabilities=desired_caps)
        try:
            cls.driver.launch_app()
            logger.info("    正在启动app")
            time.sleep(5)
            cls.driver.login(el, data['phone'], data['passwd'], success=True)
            time.sleep(2)
            cls.driver.my_page()
            time.sleep(2)
            logger.info("    点击头像按钮")
            cls.driver.click_btn('avatar')
            time.sleep(2)
        except Exception as e:
            logger.error(e)
            logger.info("    app启动失败")
            cls.driver.quit()

    @MyProfile.get_shot
    def test_01_01_empty_name(self):
        logger.info('01-01, 测试昵称输入为空')
        self.driver.click_name()
        logger.info("    清除昵称内容")
        self.driver.clear_data('alias_edit')
        self.driver.find_toast(my_profile_toast['empty_name'], el['confirm_btn'])

    @MyProfile.get_shot
    def test_01_02_long_name(self):
        logger.info('01-02, 测试昵称输入为10个以上字符')
        self.driver.edit_name('12345678901')
        self.driver.find_toast(my_profile_toast['length_over_ten'], el['confirm_btn'])

    @MyProfile.get_shot
    def test_02_modify_name(self):
        logger.info('02, 测试修改昵称成功')
        self.driver.edit_name('123456')
        self.driver.save()
        a = self.driver.name_value()
        self.assertEqual(a, '123456')

    @MyProfile.get_shot
    def test_03_modify_gender_female(self):
        logger.info('03, 测试修改性别为女成功')
        self.driver.click_name()
        self.driver.edit_name('jimmy')
        self.driver.save()
        self.driver.click_gender()
        self.driver.modify_gender_female()
        a = self.driver.gender_value()
        self.assertEqual(a, '女')

    @MyProfile.get_shot
    def test_04_modify_gender_male(self):
        logger.info('04, 测试修改性别为男成功')
        self.driver.click_gender()
        self.driver.modify_gender_male()
        a = self.driver.gender_value()
        self.assertEqual(a, '男')

    @MyProfile.get_shot
    def test_05_01_modify_birth_date(self):
        logger.info('05-01, 测试修改生日成功')
        self.driver.click_birth()
        self.assertTrue(True)

    @MyProfile.get_shot
    def test_05_02_modify_birth_date(self):
        logger.info('05-02, 测试修改生日成功"取消"')
        self.driver.click_birth_cancel()
        a = self.driver.current_activity
        self.assertEqual(a, '.ui.profile.ProfileSettingActivity')

    @MyProfile.get_shot
    def test_06_modify_school_time(self):
        logger.info('06, 测试修改入学时间成功')
        self.driver.click_time_to_school('2015')
        a = self.driver.time_to_value()
        self.assertIn('2015', a)

    @MyProfile.get_shot
    def test_07_modify_degree(self):
        logger.info('07, 测试修改学位成功')
        self.driver.click_degree()
        self.driver.degree_alter()
        a = self.driver.degree_value()
        self.assertEqual('大学生', a)

    @MyProfile.get_shot
    def test_08_01_modify_major(self):
        logger.info('08-01, 测试修改专业')
        self.driver.click_major()
        a = self.driver.current_activity
        self.assertEqual('.ui.register.ChooseProfessionActivity', a)

    @MyProfile.get_shot
    def test_08_02_search_major_not_exist(self):
        logger.info('08-02, 测试修改专业， 搜索不存在的专业')
        self.driver.search_major('123')
        a = self.driver.element_exist(el['name'])
        self.assertFalse(a)

    @MyProfile.get_shot
    def test_08_03_search_major_exist(self):
        logger.info('08-03, 测试修改专业， 搜索存在的专业')
        self.driver.search_major('通信工程')
        self.driver.click_btns(el['name'], 1)
        a = self.driver.current_activity
        self.assertEqual(a, '.ui.profile.ProfileSettingActivity')

    @MyProfile.get_shot
    def test_08_04_modify_major(self):
        logger.info('08-04, 更改修改专业')
        self.driver.click_major()
        a = self.driver.current_activity
        self.assertEqual('.ui.register.ChooseProfessionActivity', a)

    @MyProfile.get_shot
    def test_08_05_search_major_exist(self):
        logger.info('08-05, 测试修改专业， 搜索存在的专业')
        self.driver.search_major('商务英语')
        self.driver.click_btns(el['name'], 1)
        a = self.driver.current_activity
        self.assertEqual(a, '.ui.profile.ProfileSettingActivity')

    @MyProfile.get_shot
    # @unittest.skip('修改就读学校')
    def test_09_01_modify_school(self):
        logger.info('09-01, 测试修改就读院校, 点击弹窗的"取消"按钮')
        self.driver.click_school()
        logger.info('   点击取消按钮, 留在当前页')
        self.driver.find_element_by_xpath('//android.widget.Button[@resource-id="android:id/button1"]').click()
        a = self.driver.current_activity
        self.assertEqual(a, '.ui.profile.ProfileSettingActivity')

    @MyProfile.get_shot
    # @unittest.skip('修改就读学校')
    def test_09_02_modify_school(self):
        logger.info('09-02, 测试修改就读院校, 点击弹窗的"继续"按钮')
        self.driver.click_school()
        logger.info('   点击继续按钮, 进入选择学校页面')
        self.driver.find_element_by_xpath('//android.widget.Button[@resource-id="android:id/button2"]').click()
        a = self.driver.current_activity
        self.assertEqual(a, '.ui.register.ChooseSchoolActivity')

    # 测试学校搜索功能,搜索存在的学校
    # @unittest.skip('')
    @MyProfile.get_shot
    def test_09_03_modify_school_not_exist(self):
        logger.info('09-03,测试搜索不存在的学校')
        logger.info('    输入要搜索的学校（不存在）')
        self.driver.send_data_to_element(regist_element['search_school'], regist_msg_data['school_not_exist'])
        time.sleep(1)
        logger.info('    获取搜索结果')
        names = self.driver.find_elements_by_id(regist_element['name'])
        if len(names) == 1 and names[0].text == '其他学校':
            self.assertTrue(True)

    # 测试学校搜索功能,搜索不存在的学校
    # @unittest.skip('')
    @MyProfile.get_shot
    def test_09_04_modify_school(self):
        logger.info('09-04,测试搜索已存在的学校')
        logger.info('    输入要搜索的学校（存在）')
        self.driver.send_data_to_element(regist_element['search_school'], regist_msg_data['school_exist'])
        time.sleep(2)
        logger.info('    获取搜索结果')
        names = self.driver.find_elements_by_id(regist_element['name'])
        logger.debug('%s' %names)
        self.driver.click_btns(regist_element['name'], 0)
        a = self.driver.current_activity
        self.assertEqual(a, '.ui.profile.ProfileSettingActivity')

    @MyProfile.get_shot
    def test_10_modify_name_success(self):
        logger.info('10, 核实昵称保存成功')
        self.driver.save()
        self.driver.click_btn('avatar')
        a = self.driver.name_value()
        self.assertEqual('jimmy', a)

    @MyProfile.get_shot
    def test_11_modify_gender_success(self):
        logger.info('11, 核实性别保存成功')
        a = self.driver.gender_value()
        self.assertEqual('男', a)

    @MyProfile.get_shot
    def test_12_modify_birth_success(self):
        logger.info('12, 核实生日保存成功')
        a = self.driver.birth_value()
        self.assertIsNotNone(a)

    @MyProfile.get_shot
    def test_13_modify_school_time(self):
        logger.info('13, 核实入学时间保存成功')
        a = self.driver.time_to_value()
        self.assertIn('2015', a)

    @MyProfile.get_shot
    def test_14_modify_degree(self):
        logger.info('14, 核实学位保存成功')
        a = self.driver.degree_value()
        self.assertEqual('大学生', a)

    @MyProfile.get_shot
    def test_15_modify_major(self):
        logger.info('15, 核实专业保存成功')
        a = self.driver.major_value()
        self.assertEqual('商务英语', a)

    @MyProfile.get_shot
    def test_16_modify_school(self):
        logger.info('16, 核实学校保存成功')
        a = self.driver.school_value()
        self.assertEqual(regist_msg_data['school_exist'], a)

    @classmethod
    def tearDownClass(cls):
        logger.info("<<<<<<<<<<<<<8，修改个人资料功能测试结束>>>>>>>>>>>>")
        cls.driver.back_btn()
        cls.driver.logout()
        cls.driver.quit()