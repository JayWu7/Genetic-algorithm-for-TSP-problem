WUXI = {
    'MAP_SIZE': [100, 100],
    'BANKS_AMOUNT': 85,
    'PEAK_ATMS': 56,
    'CHINESE_NAME': '无锡',
    'START_POINT': {  # 初始点
        'lat': 31.525718,
        'lng': 119.324082
    },
}

SHANGHAI = {
    'MAP_SIZE': [300, 300],
    'BANKS_AMOUNT': 241,
    'PEAK_ATMS': 85,
    'CHINESE_NAME': '上海',
    'START_POINT': {
        'lat': 30.863421,
        'lng': 121.102513
    }
}

citys = {
    'WUXI': WUXI,
    'SHANGHAI': SHANGHAI,
}

EARTH_RADIUS = 6371  # 地球平均半径，6371km

# 爬虫参数
city = '上海'  # 每次爬一个城市，在这里修改
bank = '中国农业银行'  # 设定银行

ak = 'rv8dBig9OwEho07yjaAVsAPTl29QHehq'
parameters = {
    'query': bank,  # 设定查询中国农业银行的网点
    'tag': 'ATM',  # POI分类为ATM
    'region': city,
    'output': 'json',
    'ak': ak,
    'city_limit': None,
    'scope': None,
    'filter': None,
    'coord_type': None,
    'ret_coordtype': None,
    'page_size': 20,
    'page_num': 0,  # 默认为0
    'sn': None,
    'timestamp': None,
    # 详细文档查看：
    # http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi
}

# 存放地图json数据目录
STORE_DIRECTORY = './map_data'

# 遗传算法进化的次数
EVOLUTION_TIMES = 100

#连续多少次最佳路线相同，则认为找到了最优解，退出进化
STOP_TIMES = 15

# 变异概率
VARIATION_RATE = 0.3
