# packer.py
from config import PALLET_WIDTH, PALLET_DEPTH, PALLET_MAX_HEIGHT, ROTATIONS
from bin import Bin

class Packer:
    def __init__(self):
        self.bins = []
        self.items = []

    def add_bin(self, bin):
        self.bins.append(bin)

    def add_item(self, item):
        self.items.append(item)

    def pack(self):
        # 重物在下排序（符合論文與實務）
        self.items.sort(key=lambda i: -i.weight / (i.w * i.d))

        for item in self.items[:]:
            placed = False
            # 先試現有棧板
            for bin in self.bins:
                if self._try_place_in_bin(item, bin):
                    placed = True
                    break
            # 放不進去就開新棧板
            if not placed:
                new_bin = Bin(f"Pallet_{len(self.bins)+1}")
                self.add_bin(new_bin)
                self._try_place_in_bin(item, new_bin)

    def _try_place_in_bin(self, item, bin):
        if not bin.can_put_item(item):
            return False

        # 嘗試所有旋轉
        original_dims = (item.w, item.d, item.h)
        for rot in ROTATIONS:
            item.w, item.d, item.h = original_dims[rot[0]], original_dims[rot[1]], original_dims[rot[2]]

            if item.w > PALLET_WIDTH or item.d > PALLET_DEPTH:
                continue

            # Bottom-Left-Fill 策略（簡單但有效）
            for x in range(0, PALLET_WIDTH - item.w + 1, 100):
                for y in range(0, PALLET_DEPTH - item.d + 1, 100):
                    z = 0
                    # 找最低可放置高度
                    for placed in bin.items:
                        if (placed.position[0] < x + item.w and
                            placed.position[0] + placed.w > x and
                            placed.position[1] < y + item.d and
                            placed.position[1] + placed.d > y):
                            z = max(z, placed.position[2] + placed.h)

                    if z + item.h <= PALLET_MAX_HEIGHT:
                        bin.put_item(item, [x, y, z])
                        return True
        # 還原原始尺寸
        item.w, item.d, item.h = original_dims
        return False