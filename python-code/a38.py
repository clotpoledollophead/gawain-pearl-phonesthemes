import json
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, fisher_exact

# ==========================================
# 1. Load Data and Map Semantic Fields
# ==========================================
with open('pearl_gl_gr_lexicon.json', 'r', encoding='utf-8') as f:
    lexicon = json.load(f)

df = pd.read_csv('pearl_speaker_tokens.csv')
df = df[df['Speaker'] != 'Speaker']  # Clean header if present
df['Word'] = df['Word'].str.lower()

# Map semantic fields from lexicon and drop unmatched tokens
df['semantic_field'] = df['Word'].map(
    {word: data['semantic_field'] for word, data in lexicon.items()}
)
df = df.dropna(subset=['semantic_field'])

# ==========================================
# 2. Build Contingency Table (Table 6)
# ==========================================
table = (
    df.groupby(['Speaker', 'semantic_field'])
    .size()
    .unstack(fill_value=0)
    .loc[['Narrator', 'Pearl-Maiden']]
)

print("--- Table 6: Observed Token Counts ---")
print(table.to_string())

# ==========================================
# 3. Chi-Squared and Standardized Residuals (Table 7)
# ==========================================
chi2_stat, p_val, dof, expected = chi2_contingency(table.values)

print(f"\n--- Overall Chi-Squared Test ---")
print(f"X^2({dof}) = {chi2_stat:.2f}, p = {p_val:.4f}")

# Calculate residuals: (Observed - Expected) / sqrt(Expected)
residuals = (table.values - expected) / np.sqrt(expected)
residuals_df = pd.DataFrame(residuals, index=table.index, columns=table.columns)

print("\n--- Table 7: Standardized Residuals (|r| > 2 is noteworthy) ---")
print(residuals_df.round(2).to_string())

# ==========================================
# 4. Fisher's Exact Test (Grace/Virtue vs All Others)
# ==========================================
target_field = "grace/virtue"

# Isolate target vs the sum of all other fields
target_counts = table[target_field]
other_counts = table.drop(columns=[target_field]).sum(axis=1)

table_2x2 = pd.DataFrame({
    target_field: target_counts,
    'all_other_fields': other_counts
})

odds_ratio, fisher_p = fisher_exact(table_2x2)

print(f"\n--- Fisher's Exact Test: '{target_field}' ---")
print(table_2x2.to_string())
print(f"Odds Ratio = {odds_ratio:.2f}")
print(f"p-value = {fisher_p:.4f}")