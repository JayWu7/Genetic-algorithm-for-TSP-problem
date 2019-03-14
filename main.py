from city import City
from create_order import create_order
from tsp import tsp


def main():
    cn = input('请输入要调度的城市名拼音：')
    city = City(city_name=cn)  # 生成城市和atms对象
    orders = create_order(cn, city.atms)
    sp = city.start_point
    tsp(orders, sp)
    # for order in orders:
    #     print(order.offset.name, order.destination.name, order.distance)


if __name__ == '__main__':
    main()
