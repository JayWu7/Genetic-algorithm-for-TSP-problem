# Genetic-algorithm-for-TSP-problem
使用遗传算法解决TSP问题

# 各文件简介

0.本项目是一到算法题的解法，具体查看 算法题.pdf

1.数据抓取（parse_data.py）：
  调用百度地图api，获取对应城市，对应银行网点的json数据包，然后下载到本地。

2.城市对象 (city.py)
  定义城市对象类 City，主要功能是生成一个城市对象，并生成这个城市对应的atm网点集合。

3.银行网点atm对象 (atm.py)
  定义Atm类

4.计算两个atm之间的距离 (calculate_distance.py)
  根据两个点之间的经纬度不同，计算相隔距离

5.随机生成押运订单 (create_order.py)
  定义订单类Order，并根据峰值atm的数量，随机生成n(n<len(atm)//2)个订单。

6.利用遗传算法，解决tsp问题 (tsp.py)
  定义Solution类表示一个染色体，即一个订单处理顺序；定义Select表示上帝类，用来选择更好的染色体。

7.配置参数 setting.py
  将参数都集成到此文件中

8.调度各个文件 main.py
  调度并启动

# 启动方法
  run main.py
  如果要更新数据集，请到settings.py 中，修改你要爬取的城市名和银行名：
 
 *爬虫参数
 city = '上海'  # 每次爬一个城市，在这里修改
 bank = '中国建设银行'  # 设定银行

  修改完毕后，启动parse_data.py即可
  注：如果你要爬取无锡和上海之外的城市，请到settings.py 中添加一个新的城市即可，按照WUXI的格式，给它赋值
  
在settings.py 中，还可以修改遗传算法的各个参数
