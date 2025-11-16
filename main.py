# main.py
import time
from openpyxl import load_workbook
from packer import Packer
from bin import Bin
from item import Item
from visualizer import plot_pallets, plot_container

start = time.time()

wb = load_workbook("data/20251029.xlsx")
ws = wb.active
items = []
for row in ws.iter_rows(min_row=2, values_only=True):
    l, w, h, weight, qty = int(row[0]*10), int(row[1]*10), int(row[2]*10), row[3], int(row[4])
    for _ in range(qty):
        items.append(Item(f"{row[0]}×{row[1]}×{row[2]}", l, w, h, weight))

print(f"載入完成：共 {len(items)} 箱")

packer = Packer()
packer.add_bin(Bin("Pallet_1"))
for item in items: packer.add_item(item)
packer.pack()

fitted = sum(len(b.items) for b in packer.bins)
print("\n" + "="*60)
print("最終結果")
print("="*60)
print(f"總箱數     : {len(items)}")
print(f"已裝箱     : {fitted}")
print(f"未裝箱     : {len(packer.unfitted)}")
print(f"棧板數     : {len(packer.bins)} 個")
for b in packer.bins:
    if b.items: print(f"  {b}")
print(f"預估貨櫃   : {max(1, (len(packer.bins)+21)//22)} 個40呎櫃")
print(f"執行時間   : {time.time()-start:.2f} 秒")

if len(packer.unfitted) == 0:
    print("結果：全部裝完，100% 出貨")

plot_pallets(packer)
plot_container(packer)