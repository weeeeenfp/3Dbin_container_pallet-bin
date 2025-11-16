# packer.py
from config import PALLET_WIDTH, PALLET_DEPTH, PALLET_MAX_HEIGHT, ROTATIONS
from bin import Bin

class Packer:
    def __init__(self):
        self.bins = []
        self.unfitted = []

    def add_bin(self, bin): self.bins.append(bin)
    def add_item(self, item): self.unfitted.append(item)

    def pack(self):
        self.unfitted.sort(key=lambda i: -i.weight / (i.w * i.d))  # 重物在下
        while self.unfitted:
            item = self.unfitted.pop(0)
            placed = False
            for bin in self.bins:
                if self._place(item, bin):
                    placed = True; break
            if not placed:
                new_bin = Bin(f"Pallet_{len(self.bins)+1}")
                self.add_bin(new_bin)
                self._place(item, new_bin)

    def _place(self, item, bin):
        if bin.total_weight + item.weight > bin.max_weight: return False
        original = (item.w, item.d, item.h)
        for rot in ROTATIONS:
            item.rotate_to(rot)
            if item.w > PALLET_WIDTH or item.d > PALLET_DEPTH: continue
            step = 50
            for x in range(0, PALLET_WIDTH - item.w + 1, step):
                for y in range(0, PALLET_DEPTH - item.d + 1, step):
                    z = 0
                    for p in bin.items:
                        if (x < p.position[0] + p.w and x + item.w > p.position[0] and
                            y < p.position[1] + p.d and y + item.d > p.position[1]):
                            z = max(z, p.position[2] + p.h)
                    if z + item.h <= PALLET_MAX_HEIGHT:
                        bin.put_item(item, x, y, z)
                        return True
        item.w, item.d, item.h = original
        return False