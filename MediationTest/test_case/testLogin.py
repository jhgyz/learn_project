# -*- coding:utf-8 -*-

import unittest
import paramunittest
from public.log import MyLog
from public import read_config as readConfig
from public import get_data as getData
from public.my_http import Http

login_xls = getData.get_xls("mediationCase.xlsx", "login")
rc = readConfig.ReadConfig("config.ini")
http = Http()
print("tessting+++++")


@paramunittest.parametrized(*login_xls)
class Login(unittest.TestCase):
    def setParameters(self, case_name, method, username, password, result, code, msg):
        """
        :param case_name:
        :param method:
        :param username:
        :param password:
        :param retult:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.username = str(username)
        self.password = str(password)
        self.result = str(result)
        self.code = code
        self.msg = str(msg)
        self.return_json = None
        self.info = None


    def description(self):
        """
        描述
        :return:
        """
        self.case_name


    def setUp(self):
        """
        :return:
        """
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()


    def test_login(self):
        """
        test body
        :return:
        """
        #set url
        http.set_url(rc.get_interface_url("login"))
        #set data
        data = {"username": self.username, "password": self.password}
        http.set_data(data)

        #test interface
        self.return_json = http.post()

        # show return message
        getData.show_return_msg(self.return_json)

        #self.checkResult()


    def tearDown(self):
        """
        :return:
        """
        info = self.return_json.json()

        if info['code'] == 200:
            # get uer token
            token_u = info['obj']
            # 将 token 存储于内存数据库 redis server
            getData.set_header(token_u)

            cj = self.return_json.cookies._cookies
            # 遍历Cookies字典列表, 查找 Cookie 对象
            while (isinstance(cj, dict)):
                for key, session in cj.items():
                    if isinstance(session, dict):
                        cj = session
                if (not isinstance(session, dict)):
                    break

            cookie = {session.name: session.value}
            # 将 SessionID 存储于内存数据库 redis server
            getData.set_cookie(cookie)

        else:
            pass

        self.log.build_case_line(self.case_name,
                                 **{'code': str(info['code']), 'message': info['message']})

        if self.result == '0':
            self.assertEqual(info['code'], self.code)

        if self.result == '1':
            self.assertEqual(info['code'], self.code)

        print("测试结束，输出log完结\n\n")


    def checkResult(self):
        """
       check test result
       :return:
       """
        self.info = self.return_json.json()

        cj = self.return_json.cookies._cookies
        # 遍历Cookies字典列表, 查找 Cookie 对象
        while (isinstance(cj, dict)):
            for key, session in cj.items():
                if isinstance(session, dict):
                    cj = session
            if (not isinstance(session, dict)):
                break

        cookie = {session.name: session.value}
        # 将 SessionID 存储于内存数据库 redis server
        getData.set_cookie(cookie)
        # show return message
        getData.show_return_msg(self.return_json)

        if self.result == '0':
            self.assertEqual(self.info['code'], self.code)

        if self.result == '1':
            self.assertEqual(self.info['code'], self.code)


if __name__ == '__main__':
    unittest.main(verbosity=2)
