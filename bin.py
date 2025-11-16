# bin.py
class Bin:
    def __init__(self, id):
        self.id = id
        self.items = []
        self.weight = 0

    def put(self, item, x, y, z):
        item.position = [x, y, z]
        self.items.append(item)
        self.weight += item.weight

    def height(self):
        if not self.items:
            return 0
        return max(z + item.h for item in self.items for x,y,z in [item.position])

    def __repr__(self):
        return f"Bin{self.id}: {len(self.items)}箱, 高{self.height()}mm, 重{self.weight}kg"