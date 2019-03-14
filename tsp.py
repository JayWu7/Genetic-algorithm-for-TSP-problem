from random import randint, shuffle, choice, sample
from calculate_distance import get_distance_hav
from copy import copy
from settings import EVOLUTION_TIMES as et
import numpy as np


class Solution():  # 一个Solution实例对应一个染色体
    '''
        将押送问题编码化：
            每一个押送订单，对应一个出发点和一个终止点，
            对于 ’同时期‘ 出现的一批订单，使用遗传算法，找出按照什么样的顺序执行这一批订单，是总路径最短的

            注： 对于一个押送订单，其终止点必是经过出发点后下一个要到达的点，
                因为银行押送现金是非常保密的，每一次押送都会有银行的工作人员陪同，所以理论上不存在一辆车同时押送两个订单
    '''

    def __init__(self, code, orders, start_p):
        self.code = code  # 编码方式，订单下标顺序,自然数编码   #list
        self.orders = orders  # list
        self.__amount = len(self.orders)  # 当前订单数
        self.start_point = start_p  # 起始点
        self.__distance = float('inf')  # 总距离
        self.__vari_code = None  # 变异后的code
        self.__vari_distance = None  # 变异后的总距离

    def variation(self):  # 变异函数
        # if self.__amount < 100: k = 9
        # elif 100<= self.__amount < 300: k= 15
        # else: k = 20
        # 随机选择一个基因v，和code[v]进行互换

        v = randint(0, self.__amount - 1)  # 要变异的基因下标 and 一个基因
        ch = self.code.index(v)
        self.__vari_code = self.code.copy()
        self.__vari_code[v], self.__vari_code[ch] = self.code[ch], self.code[v]

        if self._fitness(flag=False) > self._fitness():  # 变异后适应性增强  #可改写减少时间消耗
            self.code = self.__vari_code
            self.__distance = self.__vari_distance

        return self.code

    def __mul__(self, other):  # 重载'*'运算符,表示交叉函数
        # = randrange(1, self.__amount // 2)
        # 随机选择一段编码，将这段编码中的基因替换为other.code对应的此段编码的基因

        n1 = randint(0, self.__amount - 1)
        n2 = randint(0, self.__amount - 1)
        if n1 > n2: n1, n2 = n2, n1

        fa, mo = copy(self), copy(other)  # 不改变父母的染色体
        while n1 <= n2:
            p, q = self.code.index(other.code[n1]), other.code.index(self.code[n1]),
            fa.code[n1], fa.code[p] = fa.code[p], fa.code[n1]
            mo.code[n1], mo.code[q] = mo.code[q], mo.code[n1]
            n1 += 1

        son = fa if fa._fitness() > mo._fitness() else mo  # 返回交叉后，更好的染色体
        return son

    def fitness(self):  # 适应度函数
        # 距离越大，倒数越小，适应性越差
        return self._fitness()

    def _fitness(self, flag=True):  # 适应度函数
        if flag:
            code = self.code
        else:
            code = self.__vari_code

        first_atm = self.orders[self.code[0]].offset
        last_atm = self.orders[self.code[-1]].destination

        fir_dis = self._get_d_start(first_atm)  # 从出发点到第一个atm的距离
        la_dis = self._get_d_start(last_atm)  # 从最后一个atm又回到出发点的距离

        distance = fir_dis + sum(self._generate_path(code)) + la_dis
        if flag:
            self.__distance = distance
        else:
            self.__vari_distance = distance

        return 1 / self.__distance  # 以距离的倒数作为适应系数

    def _get_d_start(self, atm):  # 计算某个atm距离初始点的位置
        lat0 = self.start_point['lat']
        lng0 = self.start_point['lng']
        lat1 = atm.location['lat']
        lng1 = atm.location['lng']
        return get_distance_hav(lat0, lng0, lat1, lng1)

    def _get_d(self, A, B):  # 计算两个'订单'之间的距离,一共三段 A0-A1-B0-B1
        A0_A1 = A.offset.get_distance_AB(A.destination)
        A1_B0 = A.destination.get_distance_AB(B.offset)
        B0_B1 = B.offset.get_distance_AB(B.destination)
        return A0_A1 + A1_B0 + B0_B1

    def _generate_path(self, code):
        # 生成中间路径
        for index, point in enumerate(code[:-1]):
            yield self._get_d(self.orders[point], self.orders[code[index + 1]])

    def get_distance(self):
        return self.__distance

    def get_fitness(self):
        return 1 / self.__distance


class Select():  # god对象，用来选择更好的染色体,即更快捷的路线
    def __init__(self, orders, start_point):
        self.orders = orders
        self.start_point = start_point
        self.__len_orders = len(self.orders)
        self.__size = self.__len_orders // 2 + 1  # 种群数量
        self.group = []  # 解决方案列表，即染色体列表
        self.best = None  # 最好的染色体
        self.__total_fit = None  # group中的染色体适应度总和
        self._init_group()

    def _init_group(self):  # 初始化种群
        code = list(range(self.__len_orders))
        # 先生成一个初始染色体，然后随机更改基因顺序产生新的染色体

        amount = 0
        while amount < self.__size:
            shuffle(code)
            if code not in self.group:
                amount += 1
                c = code.copy()
                solution = Solution(c, self.orders, self.start_point)
                self.group.append(solution)
        self._cam_fitness()

    def _cam_fitness(self):  # 计算每个染色体的fitness
        self.best = self.group[0]
        self.__total_fit = self.group[0].fitness()
        for so in self.group[1:]:
            so.fitness()
            self.__total_fit += so.fitness()
            if self.best.get_fitness() < so.get_fitness():
                self.best = so

    def select(self):  # 选择函数
        # 先按照基因的适应度排序
        next_gene = list()  # 下一代
        next_gene.append(self.best)  # 挑选父代中适应度最高的直接加入子代，精英选择
        # 按照fitness大小生成转盘，从group中随机挑选父母，直到生成了size/2 个子代

        prob = [s.get_fitness()/self.__total_fit for s in self.group]

        for _ in range(self.__size // 2):

            f = np.random.choice(self.group,p = prob)
            while True:
                m = np.random.choice(self.group,p = prob)
                if m != f:
                    break
            son = f * m
            next_gene.append(son)

        # # 挑选剩下的 size /2 -1 个染色体
        # for _ in range(self.__size - len(next_gene)):
        #     s0, s1 = sample(self.group, k=2)
        #     s = s0 if s0.get_fitness() > s1.get_fitness() else s1
        #     next_gene.append(s)



        self.group = next_gene  # 新老交替
        self._cam_fitness()  #重新计算每个染色体的fitness


def tsp(orders, start_point):
    nat = Select(orders, start_point)  # Select对象，nature
    print('随机生成的第一代，最优订单处理顺序为：{}，路径长度为：{}，{}'.format(nat.best.code, nat.best.get_distance(), nat.best.get_fitness()))
    for i in range(2, et + 2):
        nat.select()
        print('第{}代，最优订单处理顺序为：{}，路径长度为：{}，{}'.format(i, nat.best.code, nat.best.get_distance(), nat.best.get_fitness()))
