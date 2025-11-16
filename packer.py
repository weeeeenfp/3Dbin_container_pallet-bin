# packer.py
from config import PALLET_WIDTH, PALLET_DEPTH, PALLET_MAX_HEIGHT, ROTATIONS
from bin import Bin

class Packer:
    def __init__(self):
        self.bins = []
        self.unfitted = []

    def add_bin(self, bin):
        self.bins.append(bin)

    def add_item(self, item):
        self.unfitted.append(item)

    def pack(self):
        # 重物在下排序（論文要求）
        self.unfitted.sort(key=lambda i: -i.weight / (i.w * i.d))

        while self.unfitted:
            item = self.unfitted.pop(0)
            placed = False

            # 嘗試放入現有棧板
            for bin in self.bins:
                if self._fit_item_in_bin(item, bin):
                    placed = True
                    break

            # 若無法放入，開新棧板
            if not placed:
                new_bin = Bin(f"Pallet_{len(self.bins)+1}")
                self.add_bin(new_bin)
                self._fit_item_in_bin(item, new_bin)

    def _fit_item_in_bin(self, item, bin):
        if bin.total_weight + item.weight > bin.max_weight:
            return False

        # 嘗試所有旋轉
        for rot in ROTATIONS:
            item.rotate_to(rot)
            if item.w > PALLET_WIDTH or item.d > PALLET_DEPTH:
                continue

            # 簡單 Bottom-Left 策略（論文 Phase 1 精神）
            candidates = [(0, 0)]
            for placed in bin.items:
                x = placed.position[0] + placed.w
                y = placed.position[1]
                if x + item.w <= PALLET_WIDTH and y + item.d <= PALLET_DEPTH:
                    candidates.append((x, y))
                x = placed.position[0]
                y = placed.position[1] + placed.d
                if x + item.w <= PALLET_WIDTH and y + item.d <= PALLET_DEPTH:
                    candidates.append((x, y))

            for x, y in candidates:
                z = 0
                for placed in bin.items:
                    if (placed.position[0] < x + item.w and
                        placed.position[0] + placed.w > x and
                        placed.position[1] < y + item.d and
                        placed.position[1] + placed.d > y):
                        z = max(z, placed.position[2] + placed.h)

                if z + item.h <= PALLET_MAX_HEIGHT:
                    bin.put_item(item, x, y, z)
                    return True
        return False