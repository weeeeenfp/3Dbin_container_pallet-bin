# item.py
class Item:
    def __init__(self, name, l, w, h, weight):
        self.name = name
        self.l = l
        self.w = w
        self.h = h
        self.weight = weight
        self.position = None  # [x, y, z]

    def rotate(self, rot):
        dims = [self.l, self.w, self.h]
        self.l, self.w, self.h = dims[rot[0]], dims[rot[1]], dims[rot[2]]

    def __repr__(self):
        return f"{self.name}({self.l}×{self.w}×{self.h})"