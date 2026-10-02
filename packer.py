# packer.py
from config import PALLET_L, PALLET_W, PALLET_MAX_H, MAX_WEIGHT, ROTATIONS
from bin import Bin
from item import Item

class Packer:
    def __init__(self):
        self.bins = []
        self.unfitted = []

    def add_bin(self):
        self.bins.append(Bin(len(self.bins) + 1))
        return self.bins[-1]

    def pack(self, items):
        # 重物在下
        items.sort(key=lambda i: -i.weight)

        self.add_bin()  # 第一個棧板

        for item in items:
            # 先試既有棧板（First-Fit）
            if any(self._try_place(bin, item) for bin in self.bins):
                continue

            # 全部放不下才開新棧板；新棧板是空的，正常情況一定放得進去
            if self._try_place(self.add_bin(), item):
                continue

            # 連空棧板都裝不下（單箱本身超規），明確記錄而非默默丟掉
            item.reset_rotation()
            self.unfitted.append(item)

        return self.bins

    def _try_place(self, bin, item):
        """嘗試把 item 放進 bin，成功回傳 True。"""
        if bin.weight + item.weight > MAX_WEIGHT:
            return False

        for rot in ROTATIONS:
            item.rotate(rot)
            if item.l > PALLET_L or item.w > PALLET_W:
                continue

            # 極簡 Bottom-Left：目前僅以 (0, 0) 為基準點，往上堆到最低可行高度
            x = y = 0
            z = 0
            for other in bin.items:
                px, py, pz = other.position
                if px < x + item.l and px + other.l > x and py < y + item.w and py + other.w > y:
                    z = max(z, pz + other.h)

            if z + item.h <= PALLET_MAX_H:
                bin.put(item, x, y, z)
                return True

        item.reset_rotation()
        return False
