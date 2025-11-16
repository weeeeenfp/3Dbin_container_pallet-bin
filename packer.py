# packer.py
from config import PALLET_L, PALLET_W, PALLET_MAX_H, MAX_WEIGHT, ROTATIONS
from bin import Bin
from item import Item

class Packer:
    def __init__(self):
        self.bins = []
        self.unfitted = []

    def add_bin(self):
        self.bins.append(Bin(len(self.bins)+1))

    def pack(self, items):
        # 重物在下
        items.sort(key=lambda i: -i.weight)

        self.add_bin()  # 第一個棧板

        for item in items:
            placed = False
            for bin in self.bins:
                if bin.weight + item.weight > MAX_WEIGHT:
                    continue

                # 試 6 種旋轉
                for rot in ROTATIONS:
                    item.rotate(rot)
                    if item.l > PALLET_L or item.w > PALLET_W:
                        continue

                    # 極簡 Bottom-Left
                    x = y = 0
                    z = 0
                    for placed in bin.items:
                        px, py, pz = placed.position
                        if px < x + item.l and px + placed.l > x and py < y + item.w and py + placed.w > y:
                            z = max(z, pz + placed.h)

                    if z + item.h <= PALLET_MAX_H:
                        bin.put(item, x, y, z)
                        placed = True
                        break
                if placed:
                    break

            if not placed:
                self.add_bin()
                self.pack([item])  # 遞迴放新棧板（保證不卡）

        return self.bins