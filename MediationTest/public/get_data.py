# -*- coding:utf-8 -*-

import os
import json
from public.my_http import Http
from xlrd import open_workbook
from public import read_config as readConfig
from public.log import MyLog
import requests
import time
import redis


rc = readConfig.ReadConfig("config.ini")
ht = Http()
log = MyLog.get_log()
logger = log.get_logger()
redisClient = redis.Redis(host='10.240.70.254', port=6379,db=0)


def get_xls(xls_name, sheet_name):
    """
    获取excel表中指定sheet数据，报错到列表中返回
    :param xls_name:
    :param sheet_name:
    :return:
    """
    cls = []
    xls_path = os.path.join(readConfig.proDir, "test_case_data", xls_name)
    file = open_workbook(xls_path)
    sheet = file.sheet_by_name(sheet_name)
    sheet_nrows = sheet.nrows
    for i in range(sheet_nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls


def get_json(response, key):
    """
    获取http请求，以json返回，获取指定key的value
    :param response:
    :param key:
    :return:
    """
    return_json = response.json()
    json_value = return_json[key]
    return json_value


def set_header(header):
    token = redisClient.set("token",header)

def get_header():
    token = redisClient.get("token")
    #byte解码成string
    return token.decode('utf-8')

def set_cookie(cookie):
    ck = redisClient.set("cookies",cookie)

def get_cookie():
    cookie = redisClient.get("cookies")
    return cookie


def show_return_msg(response):
    """
    show msg detail
    :param response:
    :return:
    """
    url = response.url
    msg = response.text
    print("\nrequest url："+ url)
    #    print("\nresponse ："+'\n'+json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4).encode('utf-8'))
    print("\nresponse : " + '\n' + msg)
# ****************************** read testCase excel *********************




if __name__ == '__main__':
    xls =get_xls("mediationCase.xlsx", "login")