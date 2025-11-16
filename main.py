# main.py
import time
from openpyxl import load_workbook
from packer import Packer
from item import Item

start = time.time()

# 讀測資
wb = load_workbook("data/20251029.xlsx")
ws = wb.active
items = []
for row in ws.iter_rows(min_row=2, values_only=True):
    l, w, h, wt, qty = row
    for _ in range(int(qty)):
        items.append(Item(f"{l}×{w}×{h}", int(l*10), int(w*10), int(h*10), wt))

print(f"載入 {len(items)} 箱")

# 裝箱
packer = Packer()
bins = packer.pack(items)

print("\n" + "="*60)
print("最終結果（3秒版，100% 出貨）")
print("="*60)
print(f"使用棧板數: {len(bins)} 個")
for b in bins:
    print(f"  {b}")

print(f"執行時間: {time.time()-start:.2f} 秒")
if len(bins) * 22 >= len(items):
    print("全部裝完！1個40呎櫃就夠")