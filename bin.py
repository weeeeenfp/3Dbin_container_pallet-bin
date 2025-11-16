# bin.py
class Bin:
    def __init__(self, name):
        self.name = name
        self.items = []
        self.width = 1200
        self.depth = 1000
        self.max_height = 1650
        self.max_weight = 1500
        self.total_weight = 0

    def put_item(self, item, x, y, z):
        item.position = [x, y, z]
        self.items.append(item)
        self.total_weight += item.weight

    def get_height(self):
        if not self.items:
            return 0
        return max(item.position[2] + item.h for item in self.items)

    def __repr__(self):
        return f"{self.name}: {len(self.items)}箱, 高{self.get_height()}mm, 重{self.total_weight:.1f}kg"