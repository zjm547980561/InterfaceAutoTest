import unittest
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import common
from common import configHttp as ConfigHttp
from requests.exceptions import HTTPError


login_xls = common.get_xls("userCase.xlsx", "auto_exchange")
print(login_xls)
case = {}

Log.MyLog.get_log().logger.info(case)

localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
d = {}
auto_exchange_guid = []


@paramunittest.parametrized(*login_xls)
class AutoExchange(unittest.TestCase):
    def setParameters(self, case_name, method, balance_type, encrypted_api_key, encrypted_api_secret, exchange_guid,
                      require_api_key,require_api_secret, require_third_key, support_qr, third_key_name, title, cost,
                      language, msg):
        """
        set params
        :param case_name:
        :param method:
        :param balance_type:
        :param encrypted_api_key:
        :param encrypted_api_secret:
        :param exchange_guid:
        :param require_api_key:
        :param require_api_secret:
        :param require_third_key:
        :param support_qr:
        :param third_key_name:
        :param title:
        :param cost:
        :param language:
        :param msg:
        :return:
        """
        global case
        self.case_name = str(case_name)
        self.method = str(method)
        self.balance_type = str(balance_type)
        self.encrypted_api_key = str(encrypted_api_key)
        self.encrypted_api_secret = str(encrypted_api_secret)
        self.exchange_guid = str(exchange_guid)
        self.require_api_key = str(require_api_key)
        self.require_api_secret = str(require_api_secret)
        self.require_third_key = str(require_third_key)
        self.support_qr = str(support_qr)
        self.third_key_name = str(third_key_name)
        self.title = str(title)
        self.cost = str(cost)
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

    def is_none(self, name, ty=""):
        if 'type' == ty:
            if name == "None":
                return None
            elif not name == '':
                return int(name.split('.')[0])
            else:
                return name
        else:
            if name == "None":
                return None
            elif name == "T":
                return True
            elif name == "F":
                return False
            else:
                return name

    def delete_key(self, key, data_copy):
        if data_copy[key] is None:
            self.data.pop(key)
        else:
            pass

    def testManualExchange(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml('auto_exchange')
        configHttp.set_url(self.url)
        self.logger.info("第一步：设置url  " + self.url)

        # set data
        self.data = dict()
        if not self.method == "delete":
            self.data['encrypted_api_key'] = self.is_none(self.encrypted_api_key)
            self.data['encrypted_api_secret'] = self.is_none(self.encrypted_api_secret)
            self.data['exchange_guid'] = self.is_none(self.exchange_guid)
            self.data['require_api_key'] = self.is_none(self.require_api_key)
            self.data['require_api_secret'] = self.is_none(self.require_api_secret)
            self.data['require_third_key'] = self.is_none(self.require_third_key)
            self.data['support_qr'] = self.is_none(self.support_qr)
            self.data['third_key_name'] = self.is_none(self.third_key_name)
            self.data['title'] = self.is_none(self.title)
            self.data['cost'] = self.is_none(self.cost)
            self.data['balance_type'] = self.is_none(self.balance_type, ty='type')

        data_copy = self.data.copy()
        for key in data_copy:
            self.delete_key(key, data_copy)
        configHttp.set_data(self.data)
        self.logger.info("第二步：设置发送数据  " + str(self.data))

        # set headers
        self.headers = dict()

        if self.language == '0.0':
            self.headers['language'] = 'zh'
        else:
            self.headers['language'] = 'en'
        self.headers['Authorization'] = localReadConfig.get_headers('Authorization')
        configHttp.set_headers(self.headers)
        self.logger.info("第三步：设置头部  " + str(self.headers))
        try:
            # test interface
            if self.method == "post":
                self.return_json = configHttp.post()
            elif self.method == "delete":
                self.logger.info("准备删除自动交易记录")
                self.delete_list()
            else:
                pass
        except Exception as e:
            self.logger.error(e)
            raise Exception("请求失败")
        self.logger.info("url  " + self.url)
        self.logger.info("第四步：发送请求, 请求方法：" + self.method)

        # check result
        self.logger.info("第五步：检查结果")

        self.checkResult()

    def tearDown(self):
        """
        :return:
        """
        if not self.method == "delete":
            if self.info:
                if self.info['success']:
                    guid = self.info['balance']['guid']
                    localReadConfig.set_headers('auto_exchange_guid', guid)
                    auto_exchange_guid.append(guid)
                else:
                    pass
        else:
            pass
        self.log.build_case_line(self.case_name, self.success, self.info)
        print("测试结束，输出log完结\n\n")
        self.log.build_end_line(self.case_name)

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.success = "Fail"
        if self.return_json.status_code == 200:
            self.info = self.return_json.json()
            self.logger.info("Return result：" + str(self.info))
            try:
                if self.method == "put" and self.info['success']:
                    self.assertEqual(self.title, self.info['balance']['title'])
                    self.assertIn(self.cost, self.info['balance']['cost'])
                    self.assertEqual(self.wallet_address, self.info['balance']['wallet_address'])
                    self.assertEqual(self.wallet_type, self.info['balance']['wallet_type'])
                elif self.method == "delete":
                    self.assertEqual(self.return_json.status_code, 200)
                    self.assertTrue(self.info['success'])
                    self.success = "pass"
                else:
                    if not self.info['success']:
                        self.assertEqual(self.info['err'], case[self.case_name])
                        self.logger.info("测试通过")
                        self.success = "Pass"
                    else:
                        self.assertTrue(self.info['success'])
                        self.get_result()
                        self.logger.info("测试通过")
                        self.success = "Pass"
            except AssertionError as e:
                self.logger.error(e)
                self.logger.info("断言失败...")
                raise AssertionError
        else:
            self.logger.error("请求失败，返回的code为：" + str(self.return_json.status_code))
            raise HTTPError('Server Error')

    def get_result(self):
        self.logger.info("准备校验返回的数据")
        self.assertEqual(self.data['balance_type'], self.info['balance']['balance_type'])
        if 'title' in self.data.keys() and self.data['title']:
            self.assertEqual(self.data['title'], self.info['balance']['title'])
        else:
            self.assertIn(self.data['exchange_guid'], self.info['balance']['title'].lower())
        self.assertEqual(self.data['exchange_guid'], self.info['balance']['exchange_guid'])

    def delete_list(self):
        for item in auto_exchange_guid:
            self.url = common.get_url_from_xml('auto_exchange') + '/' + item
            configHttp.set_url(self.url)
            self.logger.info('url: ' + self.url)
            self.logger.info('headers: ' + str(self.headers))
            self.return_json = configHttp.delete()
            self.logger.info("删除记录：" + item)
