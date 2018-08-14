import unittest
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import common
from common import configHttp as ConfigHttp
import pdb


login_xls = common.get_xls("userCase.xlsx", "login")
print(login_xls)
case = {}
for item in login_xls:
    case[item[0]] = item[5]

localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*login_xls)
class Login(unittest.TestCase):
    def setParameters(self, case_name, method, email, password, language, msg):
        """
        set params
        :param case_name:
        :param method:
        :param email:
        :param password:
        :param language:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.email = str(email)
        self.password = str(password)
        self.result = str(msg)
        self.language = str(language)
        self.msg = str(msg)
        self.return_json = None
        self.info = None

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
        self.log.build_start_line(self.case_name)
        print(self.case_name + "测试开始前准备")

    def is_none(self, name):
        if name == "None":
            return None
        else:
            return name

    def testLogin(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml('login')
        configHttp.set_url(self.url)
        self.logger.info("第一步：设置url  " + self.url)

        # set data
        data = dict()
        data['email'] = self.is_none(self.email)
        if self.password:
            self.password = self.password.split('.')[0]
        data['password'] = self.is_none(self.password)
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

        # test interface
        self.return_json = configHttp.post()
        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        self.logger.info("第四步：发送请求, 请求方法：" + method)

        # check result
        self.logger.info("第五步：检查结果")
        self.checkResult()

    def tearDown(self):
        """
        :return:
        """
        self.log.build_case_line(self.case_name, self.success, self.info)
        print("测试结束，输出log完结\n\n")
        self.log.build_end_line(self.case_name)

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        self.success = "Fail"
        try:
            if not self.info['success']:
                self.assertEqual(self.info['err'], case[self.case_name])
                self.logger.info("测试通过")
                self.success = "Pass"
            else:
                self.assertTrue(self.info['user'])
                self.logger.info("测试通过")
                self.success = "Pass"
        except AssertionError as e:
            self.logger.error(e)
            self.logger.info("断言失败...")
            raise AssertionError

