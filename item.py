# item.py
class Item:
    def __init__(self, name, w, d, h, weight):
        self.name = name
        self.w = w      # width (x)
        self.d = d      # depth (y)
        self.h = h      # height (z)
        self.weight = weight
        self.position = None    # [x, y, z]
        self.rotation = 0

    def rotate_to(self, rot_idx):
        dims = [self.w, self.d, self.h]
        self.w, self.d, self.h = dims[rot_idx[0]], dims[rot_idx[1]], dims[rot_idx[2]]
        self.rotation = rot_idx

    def __repr__(self):
        return f"{self.name}({self.w}×{self.d}×{self.h}, {self.weight}kg)"