import unittest
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import common
from common import configHttp as ConfigHttp
import pdb


login_xls = common.get_xls("userCase.xlsx", "ico")
# print(login_xls)
case = {}


localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*login_xls)
class Ico(unittest.TestCase):
    def setParameters(self, case_name, method, name, coin_count, coin_cost, coin_cost_unit, currency_cost, remark, time, language, msg):
        """
        set params
        :param case_name:
        :param method:
        :param name:
        :param coin_count:
        :param coin_cost:
        :param coin_cost_unit:
        :param currency_cost:
        :param remark:
        :param time:
        :param language:
        :param msg:
        :return:
        """
        global case
        self.case_name = str(case_name)
        self.method = str(method)
        self.name = str(name)
        self.coin_count = str(coin_count)
        self.coin_cost = str(coin_cost)
        self.coin_cost_unit = str(coin_cost_unit)
        self.time = str(time)
        self.language = str(language)
        self.msg = str(msg)
        self.currency_cost = str(currency_cost)
        self.remark = str(remark)
        self.return_json = None
        self.info = None
        case[self.case_name] = self.msg

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name + "测试开始前准备")
        self.log.build_start_line(self.case_name)

    def is_none(self, name):
        if name == "None":
            return None
        else:
            return name

    def testIco(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml('ico')
        configHttp.set_url(self.url)
        self.logger.info("第一步：设置url  " + self.url)

        # set data
        data = dict()
        data['name'] = self.is_none(self.name)
        data['coin_cost'] = self.is_none(self.coin_cost)
        data['coin_cost_unit'] = self.is_none(self.coin_cost_unit)
        data['coin_count'] = self.is_none(self.coin_count)
        data['currency_cost'] = self.is_none(self.currency_cost)
        data['remark'] = self.is_none(self.remark)
        data['time'] = self.is_none(self.time)
        configHttp.set_data(data)
        self.logger.info("第二步：设置发送数据  " + str(data))

        # set headers
        headers = dict()
        if self.language == '0.0':
            headers['language'] = 'zh'
        else:
            headers['language'] = 'en'
        headers['Authorization'] = localReadConfig.get_headers('Authorization')
        configHttp.set_headers(headers)

        self.logger.info("第三步：设置头部  " + str(headers))
        self.guid = localReadConfig.get_headers('guid')
        # test interface
        if self.method == "post":
            self.return_json = configHttp.post()
        elif self.method == "get":
            self.url = self.url + '/' + self.guid
            configHttp.set_url(self.url)
            self.return_json = configHttp.get()
        elif self.method == "put":
            self.url = self.url + '/' + self.guid
            configHttp.set_url(self.url)
            self.return_json = configHttp.put()
        elif self.method == "delete":
            self.url = self.url + '/' + self.guid
            configHttp.set_url(self.url)
            configHttp.delete()
        else:
            pass
        self.logger.info("url  " + self.url)
        self.logger.info("第四步：发送请求, 请求方法：" + self.method)

        # check result
        self.logger.info("第五步：检查结果")

        self.checkResult()

    def tearDown(self):
        """
        :return:
        """
        if self.info:
            if self.info['success']:
                guid = self.info['ico_note']['guid']
                localReadConfig.set_headers('guid', guid)
            self.log.build_case_line(self.case_name, self.success, self.info)
        print("测试结束，输出log完结\n\n")
        self.log.build_end_line(self.case_name)

    def checkResult(self):
        """
        check test result
        :return:
        """
        if self.return_json:
            self.info = self.return_json.json()
        self.success = "Fail"
        try:
            if self.method == "put" and self.info['success']:
                self.assertEqual(self.name, self.info['ico_note']['name'])
                self.assertEqual(self.coin_count, self.info['ico_note']['coin_count'])
                self.assertEqual(self.coin_cost, self.info['ico_note']['coin_cost'])
                self.assertEqual(self.coin_cost_unit, self.info['ico_note']['coin_cost_unit'])
                self.assertIn(self.currency_cost, self.info['ico_note']['currency_cost'])
                self.assertEqual(self.remark, self.info['ico_note']['remark'])
            elif self.method == "delete":
                self.return_json = configHttp.get()
                self.info = self.return_json.json()
                self.assertEqual(self.info['err'], self.msg)
                self.success = 'pass'
            else:
                if not self.info['success']:
                    self.assertEqual(self.info['err'], case[self.case_name])
                    self.logger.info("测试通过")
                    self.success = "Pass"
                else:
                    self.assertTrue(self.info['ico_note'])
                    self.logger.info("测试通过")
                    self.success = "Pass"
        except AssertionError as e:
            self.logger.error(e)
            self.logger.info("断言失败...")
            raise AssertionError

