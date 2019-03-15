from calculate_distance import get_distance_hav

class Atm():
    def __init__(self, name, lo, area, addr):
        # self.uid = uid
        self.name = name
        self.location = lo
        self.area = area
        self.address = addr
        self.atm_name = self._create_only_name()

    def _create_only_name(self):
        return '{}-{}-{}'.format(self.area, self.address, self.name)

    def get_distance_AB(self,other):   #获得当前点到另一个atm的距离
        lat0 = self.location['lat']
        lng0 = self.location['lng']
        lat1 = other.location['lat']
        lng1 = other.location['lng']
        return get_distance_hav(lat0, lng0, lat1, lng1)
