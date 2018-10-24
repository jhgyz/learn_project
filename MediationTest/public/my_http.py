# -*- coding:utf-8 -*-

import requests
from public import read_config as readConfig
from public.log import MyLog
import json

import redis
redisClient = redis.Redis(host='10.240.70.254', port=6379,db=0)
rc = readConfig.ReadConfig("config.ini")

class Http:
    def __init__(self):
        self.scheme = rc.get_http("scheme")
        self.ip = rc.get_http("ip")
        self.port = rc.get_http("port")
        self.timeout = rc.get_http("timeout")
        self.headers = {}
        self.cookies = {}
        self.data = {}
        self.url = None
        self.file = {}
        self.state = {}

    def set_url(self, url):
        """
        接口路径
        :param url:
        :return:
        """
        #self.url = "%s://%s:%s%s" % (self.scheme, self.ip, self.port, url)
        self.url = "%s://%s%s" % (self.scheme, self.ip, url)

    def set_headers(self, header):
        """

        :param header:
        :return:
        """
        self.headers = header



    def set_cookies(self, cookies):
        """

        :param cookies:
        :return:
        """
        self.cookies = dict(cookies)

    def set_data(self, data):
        """
        传的参数json\params等
        :param self:
        :param data:
        :return:
        """
        self.data = data

    def get(self):
        """
        get请求
        :return:
        """
        try:
            #当headers传的cookies时，要把键值对id改成cookies
            response = requests.get(self.url, cookies=self.cookies, headers=self.headers, timeout=float(self.timeout))
            return response
        except TimeoutError as e:
            self.logger.error(e)
            return None

    def post(self):
        """
        post请求
        :return:
        """
        try:
            #当header传的cookies时，要把键值对id改成cookies
            #json参数会自动将字典类型的对象转换为json格式
            response = requests.post(self.url, cookies=self.cookies, headers=self.headers, json=self.data, timeout=float(self.timeout))
            #如果使用data参数则要手工转换一下
            #response = requests.post(self.url, cookies=self.headers, data=json.dumps(self.data), timeout=float(self.timeout))

            return response
        except TimeoutError as e:
            self.logger.error(e)
            return None

if __name__ == '__main__':
    ht = Http()
    ht.set_url(rc.get_interface_url("login"))
    ht.set_data({'username': "cm9vdA==", 'password': "cHVibGlj"})
    # res = ht.post()
    # status = res.status_code
    # print(type(status))
    res = ht.post().json()
    print(res)
