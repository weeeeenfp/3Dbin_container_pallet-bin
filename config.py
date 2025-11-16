# config.py
PALLET_WIDTH = 1200
PALLET_DEPTH = 1000
PALLET_MAX_HEIGHT = 1650    # DHL 實務上限
PALLET_MAX_WEIGHT = 1500

ROTATIONS = [
    (0, 1, 2),  # 原方向 lwh
    (0, 2, 1),  # lhw
    (1, 0, 2),  # wlh
    (1, 2, 0),  # whl
    (2, 0, 1),  # hlw
    (2, 1, 0),  # hwl
]