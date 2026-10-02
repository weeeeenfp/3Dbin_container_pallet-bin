# item.py
class Item:
    def __init__(self, name, l, w, h, weight):
        self.name = name
        self.l = l
        self.w = w
        self.h = h
        self.weight = weight
        self.position = None  # [x, y, z]
        # 保留原始尺寸：旋轉一律以原始尺寸為基準重新排列，
        # 否則連續套用多組 rotation 會疊加變換，試不到真正的 6 種方向。
        self._base_dims = (l, w, h)

    def rotate(self, rot):
        """以原始尺寸為基準，套用 rot 指定的軸排列。"""
        dims = self._base_dims
        self.l, self.w, self.h = dims[rot[0]], dims[rot[1]], dims[rot[2]]

    def reset_rotation(self):
        """還原為原始尺寸。"""
        self.l, self.w, self.h = self._base_dims

    def __repr__(self):
        return f"{self.name}({self.l}×{self.w}×{self.h})"
