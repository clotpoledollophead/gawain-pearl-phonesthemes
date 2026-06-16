import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp, mannwhitneyu

# ==========================================
# 1. Generate Timeline Data in Memory
# ==========================================
files = {'Pearl': 'pearl_cleaned.txt', 'SGGK': 'sggk_cleaned.txt'}
timeline_data = []

for poem, filepath in files.items():
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
        continue
        
    total_lines = len(lines)
    for i, line in enumerate(lines):
        # Calculate normalized position: 0.0 (first line) to 1.0 (last line)
        normalized_pos = i / (total_lines - 1) if total_lines > 1 else 0
        matches = re.findall(r'\b(gl|gr)\w*', line.lower())
        
        for cluster_prefix in matches:
            timeline_data.append({
                'text': poem,
                'cluster': cluster_prefix,
                'position': normalized_pos
            })

df = pd.DataFrame(timeline_data)
gl_df = df[df['cluster'] == 'gl']
gr_df = df[df['cluster'] == 'gr']

# ==========================================
# 2. Calculate and Print Statistics
# ==========================================
texts = ['Pearl', 'SGGK']
print(f'{"Text":<8} {"gl- median":>12} {"gr- median":>12} {"MW U":>10} {"MW p":>10} {"KS D":>10} {"KS p":>10}')
print('-' * 80)

for text in texts:
    gl_pos = np.sort(gl_df[gl_df['text'] == text]['position'].values)
    gr_pos = np.sort(gr_df[gr_df['text'] == text]['position'].values)
    
    # Mann-Whitney U Test
    U, mw_p = mannwhitneyu(gl_pos, gr_pos, alternative='two-sided')
    # Kolmogorov-Smirnov Test
    D, ks_p = ks_2samp(gl_pos, gr_pos)
    
    print(f'{text:<8} {np.median(gl_pos):>12.3f} {np.median(gr_pos):>12.3f} '
          f'{U:>10.1f} {mw_p:>10.4f} {D:>10.3f} {ks_p:>10.4f}')

# ==========================================
# 3. Generate Figure 2 (CDF Plot)
# ==========================================
plt.rcParams['font.family'] = ['Arial']
PEARL_COLOR = 'goldenrod'
SGGK_COLOR = 'forestgreen'

fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

for ax, text in zip(axes, texts):
    gl_pos = np.sort(gl_df[gl_df['text'] == text]['position'].values)
    gr_pos = np.sort(gr_df[gr_df['text'] == text]['position'].values)
    
    D, p = ks_2samp(gl_pos, gr_pos)
    
    # Calculate Empirical CDFs
    gl_ecdf = np.arange(1, len(gl_pos) + 1) / len(gl_pos)
    gr_ecdf = np.arange(1, len(gr_pos) + 1) / len(gr_pos)
    
    # Plot lines
    ax.step(gl_pos, gl_ecdf, where='post', label='gl-', linewidth=2.8, color=PEARL_COLOR)
    ax.step(gr_pos, gr_ecdf, where='post', label='gr-', linewidth=2.8, color=SGGK_COLOR)
    
    # Calculate maximum distance line (KS Statistic)
    combined = np.sort(np.concatenate([gl_pos, gr_pos]))
    gl_interp = np.searchsorted(gl_pos, combined, side='right') / len(gl_pos)
    gr_interp = np.searchsorted(gr_pos, combined, side='right') / len(gr_pos)
    
    diff = np.abs(gl_interp - gr_interp)
    max_idx = np.argmax(diff)
    x_d = combined[max_idx]
    y1, y2 = gl_interp[max_idx], gr_interp[max_idx]
    
    # Draw dashed vertical line for KS D
    ax.vlines(x_d, min(y1, y2), max(y1, y2), color='#333333', linestyle='--', linewidth=2.2)
    
    # Annotate stats
    sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
    ax.text(0.98, 0.02, f'D = {D:.3f}\np = {p:.4f}\n{sig}', 
            transform=ax.transAxes, ha='right', va='bottom', fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    
    # Formatting
    ax.set_title(text, fontsize=13)
    ax.set_xlabel('Normalized text position')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

axes[0].set_ylabel('Cumulative proportion')
axes[0].legend(frameon=False)

plt.tight_layout()
plt.savefig('figure_2_ks_ecdf.png', dpi=300, transparent=True, bbox_inches='tight')
plt.show()