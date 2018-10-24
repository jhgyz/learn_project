# -*- coding:utf-8 -*-

import unittest
import paramunittest
from public import read_config as readConfig
from public.log import MyLog
from public import get_data as getData
from public.my_http import Http


getlog_xls = getData.get_xls("mediationCase.xlsx", "getlog")
rc = readConfig.ReadConfig("config.ini")
http = Http()



@paramunittest.parametrized(*getlog_xls)
class GetSysLog(unittest.TestCase):

    def setParameters(self, case_name, method, token, result, code, msg, data):
        """
        set params
        :param case_name:
        :param method:
        :param token:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.result = str(result)
        self.code = code
        self.msg = str(msg)
        self.return_json = None
        self.info = None
        print(data)
        self.data = eval(data)
        print(self.data)
        print(type(self.data))

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
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name + "测试开始前准备")

    def testGetLog(self):
        """
        test body
        :return:
        """
        # set url
        self.url = rc.get_interface_url("getlog")
        http.set_url(self.url)
        print("第一步：设置url  " + self.url)

        # get visitor token
        if self.token == '0':
            local_token = getData.get_header()
            local_cookie = getData.get_cookie()
        elif self.token == '1':
            local_token = None

        # set headers
        header = {"Authorization": local_token}
        http.set_headers(header)

        http.set_cookies(eval(local_cookie))

        http.set_data(self.data)
        print("第三步：设置发送请求的参数")

        # test interface
        self.return_json = http.post()
        method = str(self.return_json.request)[
                 int(str(self.return_json.request).find('[')) + 1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法：" + method)

        getData.show_return_msg(self.return_json)
        # check result
        #self.checkResult()

    def tearDown(self):
        """

        :return:
        """
        info = self.return_json.json()

        self.log.build_case_line(self.case_name,**{'code': str(info['code']), 'message': info['message']})

        print("第五步：检查结果")
        if self.result == '0':
            self.assertEqual(info['code'], self.code)

        if self.result == '1':
            self.assertEqual(info['code'], self.code)

        print(u"测试结束，输出log完结\n\n")

    def checkResult(self):
        """
        check test result
        :return:
        """


        self.info = self.return_json.json()
        #show return message
        getData.show_return_msg(self.return_json)


