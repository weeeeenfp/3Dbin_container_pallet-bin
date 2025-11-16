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
    l_cm, w_cm, h_cm, weight, qty = row
    l, w, h = l_cm*10, w_cm*10, h_cm*10
    for _ in range(int(qty)):
        items.append(Item(f"{l_cm}×{w_cm}×{h_cm}", l, w, h, weight))

print(f"總共載入 {len(items)} 箱貨物")

# 建立 packer
packer = Packer()
packer.add_bin(Bin("Pallet_1"))

for item in items:
    packer.add_item(item)

print("開始裝箱...")
packer.pack()

# 結果統計
total = len(items)
fitted = sum(len(b.items) for b in packer.bins)
unfitted = total - fitted

print("\n" + "="*60)
print("最終裝箱結果")
print("="*60)
print(f"總箱數     : {total}")
print(f"已裝箱     : {fitted}")
print(f"未裝箱     : {unfitted}")

if unfitted == 0:
    print("結果：全部裝完，100% 出貨")
else:
    print("警告：有貨物未裝入（極少發生）")

print(f"\n使用棧板數 : {len(packer.bins)} 個")
for bin in packer.bins:
    if bin.items:
        print(f"  {bin}")

containers = max(1, len(packer.bins) // 22 + (1 if len(packer.bins) % 22 else 0))
print(f"\n預估 40呎貨櫃數 : {containers} 個（雙層堆疊）")
print(f"總執行時間       : {time.time() - start:.2f} 秒")