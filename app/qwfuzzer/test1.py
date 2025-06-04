from mutator_check import PromptMutator

from config import qw_api_key, gj_api_key

from Prompt_Blacklist import prompt_blacklist

import matplotlib.pyplot as plt

import numpy as np

mutator = PromptMutator(qw_api_key=qw_api_key, gj_api_key=gj_api_key)
up1, up2, down = 0, 0, 0
with open("MaliciousInstruct_data.txt", "r", encoding="utf-8") as file:
    for line in file:
        res = prompt_blacklist.check_similarity(line, threshold=0.75)
        down += 1
        # 第一重防御成功检测
        if res is True:
            up1 += 1
            up2 += 1
        else:
            ans = mutator.check_safety(line)
            # 第二重防御成功检测
            if ans is False:
                up2 += 1

print(f"仅第一重防御拦截率为:{up1 / down}")
print(f"双重防御拦截率为:{up2 / down}")

# 数据
data = [(up1 / down), (up2 / down)]
# 创建画布和样式美化
plt.figure(figsize=(8, 6), facecolor='white', dpi=100)  # 提高DPI使文字更清晰

# 绘制柱状图
bars = plt.bar(
    ["Single Barrier", "Double Barriers"],  # 英文标签
    data,
    color=['#1f77b4', '#ff7f0e'],          # 更鲜明的对比色
    width=0.5,
    edgecolor='black',
    linewidth=1.5,
    zorder=2
)

# 精确设置y轴范围（动态计算）
y_min = min(data) - 0.015  # 下限留出空间
y_max = max(data) + 0.015  # 上限留出空间
plt.ylim(y_min, y_max)

# 添加精确数据标签
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2,
        height + 0.002,  # 标签放在柱顶上方
        f'{height:.3%}', # 显示为百分比格式（如90.0%）
        ha='center',
        va='bottom',
        color='black',    # 改为黑色更清晰
        fontsize=12,
        fontweight='bold'
    )

# 坐标轴和标题美化
plt.ylabel('Defense Success Rate', fontsize=12, labelpad=10, fontweight='bold')
plt.xticks(fontsize=11, rotation=0)  # 确保x轴标签显示
plt.yticks(
    np.arange(round(y_min, 2), y_max, 0.01),  # 动态刻度
    [f'{y:.1%}' for y in np.arange(round(y_min, 2), y_max, 0.01)],  # y轴百分比格式
    fontsize=10
)

# 标题和网格线
plt.title(
    'Defense Effectiveness Comparison\n(Single vs Double Barriers)',
    fontsize=14,
    pad=20,
    fontweight='bold',
    linespacing=1.5
)
plt.grid(axis='y', linestyle=':', alpha=0.6, zorder=1)

# 移除顶部和右侧边框
ax = plt.gca()
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.show()
