# main.py
import time
from openpyxl import load_workbook
from packer import Packer
from item import Item
from visualizer import generate_html_visualization

start = time.time()

# 讀測資
wb = load_workbook("data/20251029.xlsx")
ws = wb.active
items = []
for row in ws.iter_rows(min_row=2, values_only=True):
    l, w, h, wt, qty = row
    for _ in range(int(qty)):
        items.append(Item(f"{l}×{w}×{h}", int(l * 10), int(w * 10), int(h * 10), wt))

print(f"載入 {len(items)} 箱")

# 裝箱
packer = Packer()
bins = packer.pack(items)

used_bins = [b for b in bins if b.items]
packed_count = sum(len(b.items) for b in used_bins)

print("\n" + "=" * 60)
print("裝箱結果")
print("=" * 60)
print(f"使用棧板數: {len(used_bins)} 個")
for b in used_bins:
    print(f"  {b}")

print(f"\n已裝入: {packed_count} / {len(items)} 箱 ({packed_count / len(items):.1%})")
if packer.unfitted:
    print(f"未裝入: {len(packer.unfitted)} 箱（單箱尺寸超過棧板規格）")
    for item in packer.unfitted[:10]:
        print(f"  {item}")
    if len(packer.unfitted) > 10:
        print(f"  ...其餘 {len(packer.unfitted) - 10} 箱")

print(f"執行時間: {time.time() - start:.2f} 秒")
generate_html_visualization(used_bins, items)
