# main.py
import time
from openpyxl import load_workbook
from packer import Packer
from bin import Bin
from item import Item

start = time.time()

# 讀取 Excel
wb = load_workbook("data/20251029.xlsx")
ws = wb.active

items = []
for row in ws.iter_rows(min_row=2, values_only=True):
    l_cm, w_cm, h_cm, weight, qty = row[0], row[1], row[2], row[3], int(row[4])
    l, w, h = l_cm*10, w_cm*10, h_cm*10
    for _ in range(qty):
        items.append(Item(f"{l_cm}×{w_cm}×{h_cm}", l, w, h, weight))

print(f"載入完成：共 {len(items)} 箱貨物")

# 建立 packer
packer = Packer()
packer.add_bin(Bin("Pallet_1"))

for item in items:
    packer.add_item(item)

print("開始執行裝箱（參考 IEEE Access 2024 演算法）...")
packer.pack()

# 結果輸出
fitted_count = sum(len(b.items) for b in packer.bins)
unfitted_count = len(packer.unfitted)

print("\n" + "="*60)
print("最終裝箱結果")
print("="*60)
print(f"總箱數       : {len(items)}")
print(f"已裝箱數     : {fitted_count}")
print(f"未裝箱數     : {unfitted_count}")

if unfitted_count == 0:
    print("結果：全部裝完，100% 出貨")
else:
    print("警告：以下貨物未裝入")
    for item in packer.unfitted:
        print(f"   {item}")

print(f"\n使用棧板數   : {len(packer.bins)} 個")
for i, bin in enumerate(packer.bins, 1):
    if bin.items:
        print(f"  {bin}")

containers = max(1, (len(packer.bins) + 21) // 22)
print(f"\n預估 40呎貨櫃數：{containers} 個（雙層堆疊）")
print(f"總執行時間       ：{time.time() - start:.2f} 秒")