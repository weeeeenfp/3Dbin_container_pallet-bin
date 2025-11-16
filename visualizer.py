# visualizer.py
import plotly.graph_objects as go
import os
from collections import Counter

def generate_html_visualization(bins, items, filename="結果_完整裝箱圖_論文級.html"):
    fig = go.Figure()

    # 統計尺寸 → 顏色 + 圖例
    size_count = Counter()
    for item in items:
        size_count[f"{item.l//10}×{item.w//10}×{item.h//10}cm"] += 1

    colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ]
    size_to_color = {}
    legend_added = set()
    color_idx = 0
    for size in size_count:
        size_to_color[size] = colors[color_idx % len(colors)]
        color_idx += 1

    # 所有棧板排成一列（可改成 3x3）
    offset_x = 0
    traces = []

    for bin_idx, bin in enumerate(bins):
        if not bin.items:
            continue

        for item in bin.items:
            x, y, z = item.position
            l, w, h = item.l, item.w, item.h
            size_key = f"{l//10}×{w//10}×{h//10}cm"
            color = size_to_color[size_key]

            # 主體箱子
            traces.append(go.Mesh3d(
                x=[offset_x+x, offset_x+x+l, offset_x+x+l, offset_x+x, offset_x+x, offset_x+x+l, offset_x+x+l, offset_x+x],
                y=[y, y, y+w, y+w, y, y, y+w, y+w],
                z=[z, z, z, z, z+h, z+h, z+h, z+h],
                i=[7,0,0,0,4,4,2,6,4,0,3,7],
                j=[3,4,1,2,5,6,5,5,0,1,6,3],
                k=[0,7,2,3,6,5,1,2,5,5,7,6],
                color=color,
                opacity=0.8,
                name=size_key,
                legendgroup=size_key,
                showlegend=size_key not in legend_added,
                hovertemplate=f"<b>{size_key}</b><br>棧板 {bin_idx+1}<extra></extra>"
            ))
            if size_key not in legend_added:
                legend_added.add(size_key)

            # 黑色描邊（12條邊）
            edges = [
                ([offset_x+x, offset_x+x+l], [y, y], [z, z]),
                ([offset_x+x, offset_x+x+l], [y+w, y+w], [z, z]),
                ([offset_x+x, offset_x+x], [y, y+w], [z, z]),
                ([offset_x+x, offset_x+x], [y, y+w], [z+h, z+h]),
                ([offset_x+x+l, offset_x+x+l], [y, y+w], [z, z]),
                ([offset_x+x+l, offset_x+x+l], [y, y+w], [z+h, z+h]),
                ([offset_x+x, offset_x+x+l], [y, y], [z+h, z+h]),
                ([offset_x+x, offset_x+x+l], [y+w, y+w], [z+h, z+h]),
                ([offset_x+x, offset_x+x], [y, y], [z, z+h]),
                ([offset_x+x, offset_x+x], [y+w, y+w], [z, z+h]),
                ([offset_x+x+l, offset_x+x+l], [y, y], [z, z+h]),
                ([offset_x+x+l, offset_x+x+l], [y+w, y+w], [z, z+h]),
            ]
            for ex, ey, ez in edges:
                traces.append(go.Scatter3d(x=ex, y=ey, z=ez, mode='lines',
                                          line=dict(color='black', width=4),
                                          showlegend=False, hoverinfo='none'))

        offset_x += 1600  # 棧板間距

    for trace in traces:
        fig.add_trace(trace)

    # 貨櫃方向標註
    fig.add_trace(go.Scatter3d(x=[500], y=[500], z=[100],
                              text=["← 貨櫃尾 Container Rear"],
                              mode="text", textfont=dict(size=18, color="red"), showlegend=False))
    fig.add_trace(go.Scatter3d(x=[offset_x-800], y=[500], z=[100],
                              text=["貨櫃頭 Container Head →"],
                              mode="text", textfont=dict(size=18, color="red"), showlegend=False))

    fig.update_layout(
        title="IEEE Access 2024 風格 3D 裝箱結果（167箱 → 9棧板，100%出貨）",
        scene=dict(
            xaxis_title="X → 貨櫃長度方向（尾 ←──────────→ 頭）",
            yaxis_title="Y → 貨櫃寬度",
            zaxis_title="Z → 高度 (mm)",
            aspectratio=dict(x=14, y=2, z=1.5),
            camera=dict(eye=dict(x=1.5, y=2, z=1.5))
        ),
        legend=dict(title="貨物尺寸 (cm)", itemsizing="constant"),
        width=1800, height=1000
    )

    fig.write_html(filename)
    os.startfile(filename) if os.name == 'nt' else os.system(f"open '{filename}'")
    print(f"已自動產生論文級 3D HTML 圖檔：{filename}")