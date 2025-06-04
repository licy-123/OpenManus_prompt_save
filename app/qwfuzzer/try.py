import matplotlib.pyplot as plt
import numpy as np

# Data preparation
categories = ['Open-Source Models', 'Basic Defense', 'ZhiDun System']
success_rates = {
    'min': [67, 72, 87.13],
    'max': [82, 85, 87.13],
    'mean': [74.5, 78.5, 87.13]  # Calculated midpoints for ranges
}

# Create professional chart
plt.figure(figsize=(10, 6), dpi=120)
ax = plt.subplot(111, facecolor='#f8f9fa')

# Custom color palette
colors = ['#4e79a7', '#f28e2b', '#e15759']

# Plot main line (mean values)
ax.plot(categories, success_rates['mean'],
        marker='o', markersize=8,
        color='#333333', linewidth=2.5,
        label='Average Success Rate')

# Add range indicators
for i, cat in enumerate(categories):
    ax.plot([i, i], [success_rates['min'][i], success_rates['max'][i]],
            color=colors[i], linewidth=4, alpha=0.7,
            solid_capstyle='round',
            label=f'Range ({cat})' if i == 0 else "")

# Add data point markers
for i, cat in enumerate(categories):
    ax.scatter(i, success_rates['mean'][i],
               color=colors[i], s=150, zorder=5,
               edgecolor='white', linewidth=1.5)

# Add value annotations
for i, cat in enumerate(categories):
    if i < 2:  # For ranged values
        ax.text(i, success_rates['max'][i]+1,
                f"{success_rates['min'][i]}%-{success_rates['max'][i]}%",
                ha='center', fontsize=10, fontweight='bold')
    else:  # For single value
        ax.text(i, success_rates['mean'][i]+1,
                f"{success_rates['mean'][i]:.1f}%",
                ha='center', fontsize=10, fontweight='bold')

# Chart styling
ax.set_ylim(60, 90)
ax.set_ylabel('Defense Success Rate (%)', fontsize=12, labelpad=10)
ax.set_title('AI Defense System Performance Comparison (2025)',
             fontsize=14, pad=20, fontweight='bold')

# Professional touches
ax.spines[['top', 'right']].set_visible(False)
ax.grid(axis='y', linestyle=':', color='#dee2e6', alpha=0.7)
ax.legend(frameon=False, loc='upper left', fontsize=10)

plt.tight_layout()
plt.savefig('defense_comparison_en.png', dpi=300, bbox_inches='tight')
plt.show()