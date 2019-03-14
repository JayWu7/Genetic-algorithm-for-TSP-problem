# class Atm():
#     def __init__(self, **kwargs):
#         print(type(kwargs))
#         print(kwargs)
#         for k,v in kwargs.values():
#             print(k)
#             print(1,v)
#             print(k,v)
#             self.k = v
#
#
# k = {'a': 3, 'b': 4}
# a = Atm(kwargs=k)
# # print(a.k)
import copy

class test():
    def __init__(self):
        self.a = 1
        self.b = 2

    def __repr__(self):
        return 'hello'


a = test()
print(a)
print(a.a)
print(a.b)
b = copy.copy(a)
b.a = 3
print(a.a)
print(b.a)
print(b.b)





#
# from city import City
#
# wuxi = City('shanghai')
# for k,v in wuxi.atms.items():
#     print(k,v.location)
# print(len(wuxi.atms))
