import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np

# 1. Define raw counts and line totals
# (SGGK line count adjusted to 2531 based on diplomatic transcription)
data = {
    'Poem': ['Pearl', 'SGGK'],
    'Lines': [1212, 2531],
    'gl_raw': [47, 49], # Extracted raw gl- counts
    'gr_raw': [78, 170] # Extracted raw gr- counts
}
df = pd.DataFrame(data)

# 2. Calculate Normalized Density (per 1,000 lines)
df['gl_norm'] = (df['gl_raw'] / df['Lines']) * 1000
df['gr_norm'] = (df['gr_raw'] / df['Lines']) * 1000

print("--- Normalized Density (Tokens per 1,000 Lines) ---")
print(df[['Poem', 'gl_norm', 'gr_norm']].round(2))

# 3. Fisher's Exact Test on Raw Counts
# Contingency table setup: [[Pearl gl, Pearl gr], [SGGK gl, SGGK gr]]
contingency_table = [
    [df.loc[0, 'gl_raw'], df.loc[0, 'gr_raw']],
    [df.loc[1, 'gl_raw'], df.loc[1, 'gr_raw']]
]
odds_ratio, p_value = stats.fisher_exact(contingency_table)

print("\n--- Fisher's Exact Test ---")
print(f"Odds Ratio: {odds_ratio:.4f}")
print(f"P-value: {p_value:.6f}")

# 4. Generate Figure 1: Bar Chart of Normalized Densities
labels = df['Poem']
x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 6))

# Plot bars with distinct colors
rects1 = ax.bar(x - width/2, df['gl_norm'], width, label='gl- cluster', color='#DAA520') # Goldenrod
rects2 = ax.bar(x + width/2, df['gr_norm'], width, label='gr- cluster', color='#228B22') # Forest Green

# Labels and Titles
ax.set_ylabel('Tokens per 1,000 Lines', fontsize=12)
ax.set_title('Normalized Density of gl- vs. gr- Clusters', fontsize=14, pad=15)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=12)
ax.legend(fontsize=11, frameon=False)

# Attach numeric labels above bars
ax.bar_label(rects1, fmt='%.2f', padding=3)
ax.bar_label(rects2, fmt='%.2f', padding=3)

# Aesthetic cleanup (remove top/right borders for an academic look)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()

# Save high-resolution image for the paper
plt.savefig('figure_1_normalized_density.png', dpi=300, transparent=True)
plt.show()