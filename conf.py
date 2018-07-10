import json
import os


class Conf():
    conf = {}

    # 初始化方法
    def __init__(self):
        super().__init__()
        Conf.conf = self.read_conf()

    # 读取配置文件
    @staticmethod
    def read_conf():
        # 判断配置文件是否存在
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                return json.load(f)
        else:
            return {}

    # 保存配置文件
    @staticmethod
    def save_config(data):
        with open('config.json', 'w') as f:
            json.dump(data, f)

    # 取配置项值
    @staticmethod
    def get_conf(name):
        if name in Conf.conf:
            return Conf.conf[name]
        else:
            return None

    # 修改配置项值
    @staticmethod
    def set_conf(name, value):
        Conf.conf[name] = value

