import requests
from settings import parameters, STORE_DIRECTORY, WUXI, SHANGHAI
from multiprocessing import Pool

# 调用百度地图api获得银行网点数据
base_api = 'http://api.map.baidu.com/place/v2/search?'
headers = {
    'Host': 'api.map.baidu.com',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}


def generate_page(bank_amount, _param):
    index = 0
    while bank_amount > 0:
        param = _param.copy()
        if bank_amount < 20:
            # 如果待爬数据量小于20，则只爬剩余数据数量
            param['page_size'] = bank_amount
        param['page_num'] = index
        yield param
        index += 1
        bank_amount -= 20


def parse_api(param):
    response = requests.get(base_api, headers=headers, params=param)
    print('正在爬取:{}'.format(response.request.url))
    content = response.content  # 直接使用二进制数据下载
    p = param
    down_load(content, p['page_num'], p['region'], p['query'])


def down_load(content, page, city, bank):
    filename = '{}_{}_{}.{}'.format(city, bank, page, 'json')
    path = STORE_DIRECTORY + '/' + filename
    with open(path, 'wb') as f:
        print('正在下载：{}'.format(filename))
        f.write(content)


def main():
    param = parameters
    if parameters['region'] == '无锡':
        city = WUXI
    elif parameters['region'] == '上海':
        city = SHANGHAI

    bank_amount = city['BANKS_AMOUNT']  #  need change

    # 多进程调用，加快爬取速度（此项目数据量少，可能作用不明显）
    pool = Pool()
    g = generate_page(bank_amount, param)
    pool.map(parse_api, g)


if __name__ == '__main__':
    main()
# print(response.request.url)
# print(response.text)
