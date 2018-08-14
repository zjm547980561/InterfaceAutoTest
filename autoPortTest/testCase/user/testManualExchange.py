import unittest
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import common
from common import configHttp as ConfigHttp
from requests.exceptions import ReadTimeout


login_xls = common.get_xls("userCase.xlsx", "manual_exchange")
print(login_xls)
case = {}

Log.MyLog.get_log().logger.info(case)

localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
d = {}


@paramunittest.parametrized(*login_xls)
class ManualExchange(unittest.TestCase):
    def setParameters(self, case_name, method, global_coin_guid, trade_type, exchange_name, pair, input_price,
                      input_price_type, amount, deducted, input_fee, input_fee_type, transfer_to_name, traded_at,
                      remark, language, msg):
        """
        set params
        :param case_name:
        :param method:
        :param global_coin_guid:
        :param trade_type:
        :param exchange_name:
        :param pair:
        :param input_price:
        :param input_price_type:
        :param amount:
        :param deducted:
        :param input_fee:
        :param input_fee_type:
        :param transfer_to_name:
        :param traded_at:
        :param remark:
        :param language:
        :param msg:
        :return:
        """
        global case
        self.case_name = str(case_name)
        self.method = str(method)
        self.global_coin_guid = str(global_coin_guid)
        self.trade_type = str(trade_type)
        self.exchange_name = str(exchange_name)
        self.pair = str(pair)
        self.input_price = str(input_price)
        self.input_price_type = str(input_price_type)
        self.amount = str(amount)
        self.deducted = str(deducted)
        self.input_fee_type = str(input_fee_type)
        self.traded_at = str(traded_at)
        self.transfer_to_name = str(transfer_to_name)
        self.input_fee = str(input_fee)
        self.remark = str(remark)
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
        self.url = common.get_url_from_xml('manual_exchange')
        configHttp.set_url(self.url)
        self.logger.info("第一步：设置url  " + self.url)

        # set data
        self.data = dict()
        print(self.deducted)
        if not self.method == "delete":
            self.data['global_coin_guid'] = self.is_none(self.global_coin_guid)

            self.data['amount'] = self.is_none(self.amount)
            self.data['deducted'] = self.is_none(self.deducted)
            self.data['exchange_guid'] = self.exchange_name.lower()
            self.data['input_fee_type'] = self.is_none(self.input_fee_type, ty='type')
            self.data['input_fee'] = self.is_none(self.input_fee)
            self.data['input_price'] = self.is_none(self.input_price)
            self.data['input_price_type'] = self.is_none(self.input_price_type, ty='type')
            self.data['remark'] = self.is_none(self.remark)
            self.data['trade_type'] = self.is_none(self.trade_type, ty='type')
            self.data['traded_at'] = self.is_none(self.traded_at, ty='type')
            if not self.trade_type == '3.0':
                self.data['exchange_name'] = self.is_none(self.exchange_name)
                self.data['exchange_guid'] = self.exchange_name.lower()
                self.data['input_price'] = self.is_none(self.input_price)
                self.data['pair'] = self.is_none(self.pair)
            else:
                self.data['transfer_from'] = self.is_none(self.exchange_name)
                self.data['transfer_to'] = self.is_none(self.input_price)
                self.data['transfer_from_name'] = self.is_none(self.pair)
                self.data['transfer_to_name'] = self.is_none(self.transfer_to_name)
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
                self.result = self.get_trade_list()
                self.delete_trade_list()
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
        # if self.info:
        #     if self.info['success']:
        #         if self.info['balance']['wallet_type'] == "ETH":
        #             guid = self.info['balance']['guid']
        #             localReadConfig.set_headers('wallet_ETH_guid', guid)
        #         else:
        #             guid = self.info['balance']['guid']
        #             localReadConfig.set_headers('wallet_BTC_guid', guid)
        self.log.build_case_line(self.case_name, self.success, self.info)
        print("测试结束，输出log完结\n\n")
        self.log.build_end_line(self.case_name)

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.success = "Fail"
        if self.return_json:
            self.info = self.return_json.json()
            self.logger.info("Return result：" + str(self.info))
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
                        self.get_holdings()
                        self.logger.info("测试通过")
                        self.success = "Pass"
            except AssertionError as e:
                self.logger.error(e)
                self.logger.info("断言失败...")
                raise AssertionError
        else:
            self.success = "Pass"

    def get_holdings(self):
        self.logger.info("准备请求持仓")
        self.result = self.get_trade_list()
        if self.result:
            d.setdefault(self.global_coin_guid, 0)
            d[self.global_coin_guid] = d[self.global_coin_guid] + float(self.amount) - self.is_deducted()
            holdings = round(float(self.amount) - self.is_deducted() + float(self.result['manual_count']) - 10, 1)
            self.assertTrue(self.result['success'])
            self.assertEqual(self.result['holding_count'], str(holdings))
            self.assertIsNotNone(self.result['holding_value'])
            self.assertIsNotNone(self.result['change_24h'])
            self.assertIsNotNone(self.result['manual_count'])
            self.assertIsNotNone(['auto_count'])
            self.assertEqual(self.result['holding_count'], str(holdings))
            self.write_trade_id()
        else:
            pass

    def transfer_fee(self):
        if not self.input_fee == "None" and not self.input_fee == "":
            input_fee = float(self.input_fee)
        else:
            input_fee = 0

        if self.input_fee_type == '1.0':
            input_fee_type = 0.01
        elif self.input_fee_type == '2.0':
            input_fee_type = 1
        else:
            input_fee_type = 0
        return input_fee_type * input_fee

    def is_deducted(self):
        if self.deducted == "FALSE":
            return 0
        else:
            return self.transfer_fee()

    def write_trade_id(self):
        localReadConfig.set_headers('series_id', self.result['trades'][-1]['series_id'])

    def delete_trade_list(self):
        for item in self.result["trades"]:
            self.url = common.get_url_from_xml('manual_exchange') + '/' + item['series_id']
            configHttp.set_url(self.url)
            configHttp.delete()
            self.logger.info("删除交易记录：" + item['series_id'])

    def get_trade_list(self):
        self.url = common.get_url_from_xml('global_coins') + '/' + self.global_coin_guid + '/holdings'
        configHttp.set_url(self.url)
        configHttp.set_headers(self.headers)
        configHttp.set_data({})
        self.logger.info("url: " + self.url)
        self.logger.info("headers: " + str(self.headers))
        configHttp.set_data({})
        response = configHttp.get()
        if response.status_code == 200:
            return configHttp.get().json()
        else:
            self.logger.error(response.text)
            return None
