# visualizer.py
import plotly.graph_objects as go
import webbrowser
import os

from config import PALLET_WIDTH, PALLET_DEPTH, PALLET_MAX_HEIGHT


def plot_pallets(packer, filename="結果_棧板裝箱圖.html"):
    fig = go.Figure()
    colors = ["#4CAF50", "#2196F3", "#9C27B0", "#FF9800", "#F44336", "#3F51B5", "#E91E63", "#607D8B"]
    for idx, bin in enumerate(packer.bins):
        if not bin.items:
            continue
        for item in bin.items:
            x, y, z = item.position
            l, w, h = item.w, item.d, item.h
            color = colors[idx % len(colors)]
            fig.add_trace(go.Mesh3d(
                x=[x, x+l, x+l, x, x, x+l, x+l, x],
                y=[y, y, y+w, y+w, y, y, y+w, y+w],
                z=[z, z, z, z, z+h, z+h, z+h, z+h],
                i=[7, 0, 0, 0, 4, 4, 2, 6, 4, 0, 3, 7],
                j=[3, 4, 1, 2, 5, 6, 5, 5, 0, 1, 6, 3],
                k=[0, 7, 2, 3, 6, 5, 1, 2, 5, 5, 7, 6],
                color=color, opacity=0.7, flatshading=True
            ))
            # 添加棧板邊框
            fig.add_trace(go.Scatter3d(
                x=[0, PALLET_WIDTH, PALLET_WIDTH, 0, 0],
                y=[0, 0, PALLET_DEPTH, PALLET_DEPTH, 0],
                z=[0, 0, 0, 0, 0],
                mode='lines', line=dict(color='black', width=2),
                showlegend=False
            ))

        # 添加棧板高度標籤
        height = bin.get_height()
        fig.add_trace(go.Scatter3d(
            x=[PALLET_WIDTH/2], y=[PALLET_DEPTH/2], z=[height/2],
            text=[f"{bin.name}<br>Height: {height}mm"],
            mode='text', textfont=dict(size=12, color="black")
        ))

    fig.update_layout(
        title="IEEE Access 2024 - 棧板裝箱結果（可拖曳旋轉）",
        scene=dict(
            xaxis_title="長度 (mm)", yaxis_title="寬度 (mm)", zaxis_title="高度 (mm)",
            aspectratio=dict(x=1.2, y=1, z=0.8),
            xaxis=dict(range=[0, PALLET_WIDTH]), yaxis=dict(range=[0, PALLET_DEPTH]), zaxis=dict(range=[0, PALLET_MAX_HEIGHT]),
            bgcolor="white"
        ),
        width=1200, height=800,
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False
    )
    fig.write_html(filename)
    webbrowser.open('file://' + os.path.realpath(filename))
    print(f"已產生：{filename}")

def plot_container(packer, filename="結果_貨櫃排板圖.html"):
    fig = go.Figure()
    C_L, C_W, C_H = 12032, 2352, 2393  # 40呎高櫃內部尺寸
    # 畫貨櫃外框
    fig.add_trace(go.Scatter3d(
        x=[0, C_L, C_L, 0, 0, C_L, C_L, 0],
        y=[0, 0, C_W, C_W, 0, 0, C_W, C_W],
        z=[0, 0, 0, 0, C_H, C_H, C_H, C_H],
        mode='lines', line=dict(color='black', width=4)
    ))

    # 放置棧板
    for i, bin in enumerate(packer.bins):
        if not bin.items:
            continue
        x = (i % 4) * 1200
        y = (i // 4) * 1000
        z = 0
        fig.add_trace(go.Mesh3d(
            x=[x, x+1200, x+1200, x, x, x+1200, x+1200, x],
            y=[y, y, y+1000, y+1000, y, y, y+1000, y+1000],
            z=[z, z, z, z, z+1650, z+1650, z+1650, z+1650],
            opacity=0.3, color='#B0BEC5'
        ))
        fig.add_trace(go.Scatter3d(
            x=[x+600], y=[y+500], z=[825],
            text=[f"{bin.name}<br>H: {bin.get_height()}mm"],
            mode='text', textfont=dict(size=10, color="black")
        ))

    fig.update_layout(
        title="40呎貨櫃排板圖（雙層可疊）",
        scene=dict(
            xaxis_title="長度 (mm)", yaxis_title="寬度 (mm)", zaxis_title="高度 (mm)",
            aspectratio=dict(x=5, y=1, z=1),
            xaxis=dict(range=[0, C_L]), yaxis=dict(range=[0, C_W]), zaxis=dict(range=[0, C_H]),
            bgcolor="white"
        ),
        width=1200, height=600,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    fig.write_html(filename)
    webbrowser.open('file://' + os.path.realpath(filename))
    print(f"已產生：{filename}")