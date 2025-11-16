# packer.py - 完全符合 IEEE Access 2024 + DHL 規範
from config import RealWorld, ROTATIONS
from loader import Item
from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass
class Box3D:
    item_id: int
    x: float; y: float; z: float
    l: float; w: float; h: float
    weight: float
    support: float = 1.0

class Pallet:
    def __init__(self, pid: int):
        self.id = pid
        self.name = f"P120_Pallet_{pid:02d}"
        self.boxes: List[Box3D] = []
        self.support_surfaces: Dict[float, List[Tuple[float,float,float,float]]] = {0.0: [(0,0,RealWorld.PALLET_L,RealWorld.PALLET_W)]}
        self.current_height = 0.0

    def can_place(self, l, w, h, weight, item_id) -> Tuple[bool, float, float, float]:
        # 只考慮現有層頂部（DHL 不允許懸空）
        candidate_zs = [0.0] + [b.z + b.h for b in self.boxes]
        
        for z in sorted(candidate_zs):
            if z + h > RealWorld.PALLET_MAX_LOAD_H:
                continue
            # 嘗試兩種旋轉
            for dl, dw in [(l,w), (w,l)]:
                if dl > RealWorld.PALLET_L or dw > RealWorld.PALLET_W:
                    continue
                # 強制靠左下角（DHL 要求齊平）
                x, y = 0.0, 0.0
                if x + dl > RealWorld.PALLET_L or y + dw > RealWorld.PALLET_W:
                    continue
                
                # 計算支撐率（論文 + DHL 要求）
                supported = 0.0
                total = dl * dw
                for sx, sy, sl, sw in self.support_surfaces.get(z, []):
                    ox = max(x, sx); oy = max(y, sy)
                    ex = min(x+dl, sx+sl); ey = min(y+dw, sy+sw)
                    if ox < ex and oy < ey:
                        supported += (ex-ox)*(ey-oy)
                if supported / total >= RealWorld.MIN_SUPPORT_RATIO:
                    return True, x, y, z
        return False, 0, 0, 0

    def place(self, l, w, h, weight, item_id):
        placed, x, y, z = self.can_place(l, w, h, weight, item_id)
        if not placed:
            return False
        
        # 選擇最佳旋轉（面積最大者優先）
        best_l, best_w = l, w
        if w > l:
            best_l, best_w = w, l
        
        self.boxes.append(Box3D(item_id, x, y, z, best_l, best_w, h, weight))
        new_top = z + h
        
        # 更新支撐面
        if new_top not in self.support_surfaces:
            self.support_surfaces[new_top] = []
        self.support_surfaces[new_top].append((x, y, best_l, best_w))
        self.current_height = max(self.current_height, z + h)
        return True

def pack_dhl_ieee_compliant(items: List[Item]) -> List[Pallet]:
    # 展開 + 重物在下排序（論文 + DHL 雙重要求）
    all_boxes = []
    for item in items:
        for _ in range(item.qty):
            density = item.weight / (item.l * item.w)  # 每單位底面積重量
            all_boxes.append((item.l, item.w, item.h, item.weight, item.id, density))
    all_boxes.sort(key=lambda x: -x[5])  # 重物優先

    pallets = []
    pallet_id = 1
    
    i = 0
    while i < len(all_boxes):
        pallet = Pallet(pallet_id)
        placed_in_this = 0
        
        j = i
        while j < len(all_boxes):
            l, w, h, wt, iid, _ = all_boxes[j]
            if pallet.place(l, w, h, wt, iid):
                all_boxes.pop(j)
                placed_in_this += 1
            else:
                j += 1
                
        if placed_in_this > 0:
            pallets.append(pallet)
            pallet_id += 1
            i = 0  # 重新從頭試（允許零頭填補）
        else:
            i += 1
            
    print(f"實務裝箱完成：共 {len(pallets)} 個棧板（每板高度 ≤ {RealWorld.PALLET_MAX_TOTAL_H}mm）")
    return pallets