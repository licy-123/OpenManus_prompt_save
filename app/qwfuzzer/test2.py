from mutator_check import PromptMutator

from config import qw_api_key, gj_api_key

from Prompt_Blacklist import prompt_blacklist

import matplotlib.pyplot as plt

from matplotlib.ticker import PercentFormatter

mutator = PromptMutator(qw_api_key=qw_api_key, gj_api_key=gj_api_key)
up1, up2, down = 0, 0, 0
with open("HarmBench_data.txt", "r", encoding="utf-8") as file:
    for line in file:
        res = prompt_blacklist.check_similarity(line, threshold=0.75)
        down += 1
        # 第一重防御成功检测
        if res is True:
            up2 += 1
        else:
            ans = mutator.check_safety(line)
            # 第二重防御成功检测
            if ans is False:
                up2 += 1

print(f"第二重防御拦截率为:{up2 / down}")

# 数据
defense_rate = up2 / down

# 创建专业级图表
plt.figure(figsize=(10, 6), facecolor='#f5f5f5', dpi=120)
ax = plt.subplot(111, facecolor='#f5f5f5')

# 绘制单柱状图（创新设计）
bar = ax.bar(
    ["Double Barrier Defense"],  # 标签名称
    [defense_rate],             # 防御率数据
    width=0.6,
    color='#2ca02c',            # 成功绿色
    edgecolor='#1a1a1a',
    linewidth=1.5,
    zorder=2
)

# 添加立体效果阴影
bar[0].set_hatch('////')
bar[0].set_alpha(0.9)

# 添加精确数据标签（动态位置）
height = bar[0].get_height()
label_y = height + 0.01 if height < 0.95 else height - 0.03
ax.text(
    0,  # x坐标（单柱居中）
    label_y,
    f'{defense_rate:.2%}',  # 百分比格式显示
    ha='center',
    va='bottom',
    color='#1a1a1a',
    fontsize=24,
    fontweight='bold',
    fontfamily='Arial'
)

# 设置y轴为百分比格式
ax.yaxis.set_major_formatter(PercentFormatter(1.0))
plt.ylim(0, 1.1)  # 留出顶部空间

# 添加参考线
ax.axhline(defense_rate, color='#d62728', linestyle=':', linewidth=1.5, alpha=0.7)

# 图表元素美化
plt.title(
    'AI Defense System Effectiveness\n(Double Barrier Protection)',
    fontsize=16,
    pad=20,
    fontweight='bold',
    color='#333333'
)
plt.ylabel(
    'Attack Interception Rate',
    fontsize=12,
    labelpad=15,
    fontweight='bold',
    color='#555555'
)

# 移除冗余边框
for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#888888')

# 添加自定义网格
ax.set_axisbelow(True)
ax.grid(
    axis='y',
    color='white',
    linestyle='-',
    linewidth=1.5,
    alpha=0.7
)

# 添加图例说明
ax.plot([], [], color='#2ca02c', linewidth=10, label='Actual Defense Rate')
ax.plot([], [], color='#d62728', linestyle=':', linewidth=2, label='Reference Line')
plt.legend(
    frameon=False,
    loc='upper right',
    fontsize=10,
    handlelength=1.5
)

# 底部添加数据来源说明
plt.text(
    0.5, -0.15,
    f'Data Source: HarmBench dataset | Total samples: {down}',
    ha='center',
    va='center',
    transform=ax.transAxes,
    fontsize=9,
    color='#777777'
)

plt.tight_layout()

# 保存高清图片（可根据需要调整）
plt.savefig('defense_performance.png', dpi=300, bbox_inches='tight', facecolor='#f5f5f5')
plt.show()
