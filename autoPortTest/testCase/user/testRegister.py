import unittest
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import common
from common import configHttp as ConfigHttp
from common.verify_code import Web


login_xls = common.get_xls("userCase.xlsx", "register")
# print(login_xls)
case = {}


localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*login_xls)
class Register(unittest.TestCase):
    def setParameters(self, case_name, method, send_email, email, password, code, device_type, language, msg):
        """
        set params
        :param case_name:
        :param method:
        :param send_email:
        :param email:
        :param password:
        :param code:
        :param device_type:
        :param language:
        :param msg:
        :return:
        """
        global case
        self.case_name = str(case_name)
        self.method = str(method)
        self.send_email = str(send_email)
        self.email = str(email)
        self._email = str(email)
        self.password = str(password)
        self.code = str(code)
        self.device_type = str(device_type)
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

    def register_ok(self):
        if self.send_email == '1.0':
            web = Web()
            self.web = web
            self.web.open_http()
            self.email = self.web.get_email
            self._email = self.email
        elif self.send_email == '2.0':
            web = Web()
            self.web = web
            self.web.open_http()
            self.email = self.web.get_email
        else:
            pass

    def _register(self):
        if self.send_email == '1.0':
            self.code = self.web.get_code
        elif self.send_email == '2.0':
            self.code = self.web.get_code
        else:
            pass

    def register_email(self):
        url = common.get_url_from_xml('register_email')
        configHttp.set_url(url)
        email = self.email
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        configHttp.set_headers(header)
        d = {'email': email}
        configHttp.set_data(d)
        configHttp.post()
        self.logger.info("url: "+url+" header: " + str(header) + " data: " + str(d))

    def testRegister(self):
        """
        test body
        :return:
        """
        # set url
        self.register_ok()
        self.register_email()
        self.logger.info("正在请求验证码...")
        self._register()
        self.url = common.get_url_from_xml('register')
        configHttp.set_url(self.url)
        self.logger.info("第一步：设置url  " + self.url)
        # set data
        data = dict()
        data['email'] = self.is_none(self._email)
        data['password'] = self.is_none(self.password)
        data['code'] = self.is_none(self.code)
        data['device_type'] = self.is_none(self.device_type)
        configHttp.set_data(data)
        self.logger.info("第二步：设置发送数据  " + str(data))

        # set headers
        headers = dict()
        if self.language == '0.0':
            headers['language'] = 'zh'
        else:
            headers['language'] = 'en'
        configHttp.set_headers(headers)

        self.logger.info("第三步：设置头部  " + str(headers))
        self.guid = localReadConfig.get_headers('guid')
        # test interface
        if self.method == "post":
            self.return_json = configHttp.post()
        else:
            pass
        self.logger.info("url  " + self.url)
        self.logger.info("第四步：发送请求, 请求方法：" + self.method)

        # check result

        self.checkResult()
        self.logger.info("第五步：检查结果")

    def tearDown(self):
        """
        :return:
        """
        if not self.send_email == '0.0':
            self.logger.info("正在关闭网页...")
            self.web.driver.quit()
        else:
            pass
        if self.info:
            if self.info['success']:
                token = self.info['user']['token']
                token = 'Token token=' + token
                localReadConfig.set_headers('authorization', token)
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
            self.logger.info(self.info)
        self.success = "Fail"
        try:
            if not self.info['success']:
                self.assertEqual(self.info['err'], case[self.case_name])
                self.logger.info("测试通过")
                self.success = "Pass"
            else:
                self.assertIsNotNone(self.info['user']['token'])
                self.logger.info("测试通过")
                self.success = "Pass"
        except AssertionError as e:
            self.logger.error(e)
            self.logger.info("断言失败，正在关闭网页...")
            self.web.driver.quit()
            raise AssertionError

