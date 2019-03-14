from settings import citys, STORE_DIRECTORY
import numpy as np
from collections import OrderedDict
import os
import json
from atm import Atm


class City():
    def __init__(self, city_name):  # 传入城市的拼音
        if city_name.upper() in citys:
            city = citys[city_name.upper()]
            self.name = city_name
            self.name_zh = city['CHINESE_NAME']
            self.map = np.zeros(city['MAP_SIZE'])
            self.banks_amount = city['BANKS_AMOUNT']
            self.peak_atm = city['PEAK_ATMS']
            self.start_point = city['START_POINT']
            self.atms = OrderedDict()
            self.__init_atms(self.name_zh)
            print('{},生成成功'.format(self.name_zh))
        else:
            raise KeyError('城市名错误，目前仅支持‘wuxi’，‘shanghai’')

    def __init_atms(self, cn):
        self._read_atm_file(cn)

    def _read_atm_file(self, cn):  # 初始化atm字典
        def helper(fn):
            if fn[0] == cn[0] and fn[1] == cn[1]:
                return True
            return False

        files = filter(helper, os.listdir(STORE_DIRECTORY))
        cur_path = os.getcwd()
        os.chdir(STORE_DIRECTORY)  # 切换目录，方便读取文件
        for fi in files:
            with open(fi, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._generate_atm_obj(data)

        os.chdir(cur_path)  # 把运行目录切换回去，防止出错

    def _generate_atm_obj(self, json_obj):
        if 'results' in json_obj:
            for bank in json_obj['results']:
                uid = bank['uid']  # poi唯一标识符
                name = bank['name']
                lo = bank['location']
                area = bank['area']  # 所在区
                addr = bank['address']  # 所在街道地址
                atm = Atm(name, lo, area, addr)
                self.atms[uid] = atm  # 唯一的uid作为键，值为atm对象实例
