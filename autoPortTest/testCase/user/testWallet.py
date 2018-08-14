import unittest
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import common
from common import configHttp as ConfigHttp
from requests.exceptions import ReadTimeout
import pdb


login_xls = common.get_xls("userCase.xlsx", "wallet")
print(login_xls)
case = {}

Log.MyLog.get_log().logger.info(case)

localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*login_xls)
class Wallet(unittest.TestCase):
    def setParameters(self, case_name, method, balance_type, cost, title, wallet_address, wallet_type, language, msg):
        """
        set params
        :param case_name:
        :param method:
        :param balance_type:
        :param cost:
        :param title:
        :param wallet_address:
        :param wallet_type:
        :param language:
        :param msg:
        :return:
        """
        global case
        self.case_name = str(case_name)
        self.method = str(method)
        self.balance_type = 2
        self.cost = str(cost)
        self.title = str(title)
        self.wallet_address = str(wallet_address)
        self.wallet_type = str(wallet_type)
        self.language = str(language)
        self.msg = str(msg)
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

    @property
    def guid(self):
        if self.wallet_type == "ETH":
            self.wallet_id = localReadConfig.get_headers('wallet_ETH_guid')
        else:
            self.wallet_id = localReadConfig.get_headers('wallet_BTC_guid')
        return self.wallet_id

    def testWallet(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml('wallet')
        configHttp.set_url(self.url)
        self.logger.info("第一步：设置url  " + self.url)

        # set data
        data = dict()
        data['balance_type'] = self.is_none(self.balance_type)
        data['cost'] = self.is_none(self.cost)
        data['title'] = self.is_none(self.title)
        data['wallet_address'] = self.is_none(self.wallet_address)
        data['wallet_type'] = self.is_none(self.wallet_type)
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
        try:
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
        except ReadTimeout as e:
            self.logger.error(e)
            raise ReadTimeout
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
                if self.info['balance']['wallet_type'] == "ETH":
                    guid = self.info['balance']['guid']
                    localReadConfig.set_headers('wallet_ETH_guid', guid)
                else:
                    guid = self.info['balance']['guid']
                    localReadConfig.set_headers('wallet_BTC_guid', guid)
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
                self.assertEqual(self.title, self.info['balance']['title'])
                self.assertIn(self.cost, self.info['balance']['cost'])
                self.assertEqual(self.wallet_address, self.info['balance']['wallet_address'])
                self.assertEqual(self.wallet_type, self.info['balance']['wallet_type'])
            elif self.method == "delete":
                self.return_json = configHttp.get()
                self.info = self.return_json.json()
                self.assertEqual(self.info['err'], self.msg)
                self.success = "pass"
            else:
                if not self.info['success']:
                    self.assertEqual(self.info['err'], case[self.case_name])
                    self.logger.info("测试通过")
                    self.success = "Pass"
                else:
                    self.assertTrue(self.info['success'])
                    self.assertEqual(self.title, self.info['balance']['title'])
                    self.assertIn(self.cost, self.info['balance']['cost'])
                    self.assertEqual(self.wallet_address, self.info['balance']['wallet_address'])
                    self.assertEqual(self.wallet_type, self.info['balance']['wallet_type'])
                    self.logger.info("测试通过")
                    self.success = "Pass"
        except AssertionError as e:
            self.logger.error(e)
            self.logger.info("断言失败...")
            raise AssertionError

