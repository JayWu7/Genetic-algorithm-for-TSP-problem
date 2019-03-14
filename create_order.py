'''生成押运订单'''
'''押运订单理解： 从一个网点取钱，然后放到另一个网点'''
from random import randint, sample
from settings import citys


class Order():
    def __init__(self, of, de):
        # 与这次订单有关的两个网点
        self.offset = of
        self.destination = de

        self.distance = self._distance()

    def _distance(self):
        return self.offset.get_distance_AB(self.destination)

    def __repr__(self):  # 打印出生成的订单信息
        return 'from：{}, to: {}'.format(self.offset.atm_name, self.destination.atm_name)


# 随机生成订单函数
def create_order(ct, atm_dic):
    # 根据高峰ATM数量来设定同一时期最大订单数
    city = citys[ct.upper()]
    peak_atm = city['PEAK_ATMS']

    # 一个订单对应两个atm
    peak_order = peak_atm // 2

    order_amount = randint(1, peak_order)  # 随机生成订单数

    random_index = sample(range(len(atm_dic)), k=order_amount * 2)  # 随机获取atm下标;确保k为偶数

    atms = []  # 存储随机生成的atm网点
    for index, (_, atm) in enumerate(atm_dic.items()):
        if index in random_index:
            atms.append(atm)

    ords = list()  # 存储随机生成的订单
    for i in range(0, order_amount * 2, 2):  # 遍历atms,偶数下标为出发点，奇数下标为到达点
        off, des = atms[i], atms[i + 1]
        order = Order(off, des)
        ords.append(order)

    _print_ords(ords)
    return ords


def _print_ords(ords):
    print('共随机生成：{}个订单，分别是： '.format(len(ords)))
    for index, ord in enumerate(ords):
        print('订单{}：{}'.format(index, ord))
