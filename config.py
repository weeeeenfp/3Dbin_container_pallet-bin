# config.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Dimensions:
    PALLET = (1200, 1000, 1800)          # mm
    CONTAINER = (12032, 2352, 2393)      # 40呎高櫃內尺寸
    MIN_SPACE_VOLUME = 100*100*100

ROTATIONS = [(0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)]
COLORS = ["#FF6B6B","#4ECDC4","#45B7D1","#96CEB4","#FECA57",
          "#DDA0DD","#98D8C8","#F7DC6F","#BB88FF","#78D5E3"]