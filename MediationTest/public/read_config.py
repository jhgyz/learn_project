# -*- coding:utf-8 -*-

import os
import configparser

#os.path.abspath(__file__)返回的是.py文件的绝对路径
proDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
conf_path = proDir + r"\config\\"

class ReadConfig:
    """
    创建ConfigParser对象，读取指定目录conf_path的配置文件config_name
    """
    def __init__(self, config_name):
        self.conf = configparser.ConfigParser()
        #中文乱码问题需要添加encoding="utf-8-sig"
        self.conf.read(conf_path + config_name, encoding="utf-8-sig")

    def get_http(self, name):
        value = self.conf.get("HTTP", name)
        return value

    def get_interface_url(self, name):
        value = self.conf.get("INTERFACE_URL", name)
        return value

if __name__ == '__main__':
    rc = ReadConfig("config.ini")
    print(rc.get_http("ip"))
    print(proDir)
    print(conf_path)