# -*- coding:utf-8 -*-

import unittest
import paramunittest
from public import read_config as readConfig
from public.log import MyLog
from public import get_data as getData
from public.my_http import Http



operatetask_xls = getData.get_xls("mediationCase.xlsx", "operatetask")
rc = readConfig.ReadConfig("config.ini")
http = Http()



@paramunittest.parametrized(*operatetask_xls)
class OperateTask(unittest.TestCase):

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
        self.data = eval(data)
        self.success = 'True'

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

    def testGetCurTask(self):
        """
        test body
        :return:
        """
        # set url
        self.url = rc.get_interface_url("operateTask")
        http.set_url(self.url)
        print("第一步：设置url  " + self.url)

        # get visitor token
        if self.token == '0':
            local_token = getData.get_header()
            local_cookie = getData.get_cookie()
        elif self.token == '1':
            token = None

        # set headers
        header = {"Authorization": local_token}
        http.set_headers(header)
        http.set_cookies(eval(local_cookie))

        print("第二步：设置header(token等)")

        # set params
        http.set_data(self.data)
        print("第三步：设置发送请求的参数")

        # test interface
        self.return_json = http.post()
        method = str(self.return_json.request)[
                 int(str(self.return_json.request).find('[')) + 1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法：" + method)

        getData.show_return_msg(self.return_json)

    def tearDown(self):
        """

        :return:
        """
        info = self.return_json.json()

        self.log.build_case_line(self.case_name,
                                 **{'code': str(info['code']), 'message': info['obj']})

        print("第五步：检查结果")
        if info['code'] == 200:
            if self.result == '0':
                self.assertEqual(str(info['success']), self.success)

            if self.result == '1':
                self.assertEqual(str(info['success']), self.success)

            print(u"测试结束，输出log完结\n\n")





