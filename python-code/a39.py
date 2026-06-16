import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, chi2, fisher_exact

# ── MED-based semantic field mapping ────────────────────────────────────────
# Words are grouped by MED category to save vertical space, 
# then flattened into the final med_map dictionary.

med_categories = {
    'joy_festivity':    ['glad', 'glade', 'gladloker', 'gladly', 'glaum', 'gle', 'glorious', 'grace', 'gracios', 'graciously'],
    'light_colour':     ['grene', 'grener', 'grenne', 'gray', 'graye', 'grayes', 'grayn', 'glem', 'glemed', 'glemered', 'glent', 'glode', 'glodes', 'glod', 'glyzt', 'glyterande', 'glytered', 'glowande', 'glede', 'gledez', 'gres', 'gresse'],
    'sound_noise':      ['glam', 'grone', 'groned', 'gronyed', 'gruch', 'gruchyng'],
    'emotion_morality': ['grame', 'gref', 'grem', 'greme', 'glopnyng', 'greue', 'greued', 'greuez', 'gryndel', 'gryndellayk', 'gryndelly', 'grymme', 'gryed', 'grwe'],
    'size_greatness':   ['gret', 'grete', 'grett', 'grattest', 'grounde', 'grounden', 'groundez', 'growe', 'gryndelston'],
    'action_motion':    ['glydande', 'glydez', 'glyfte', 'grayth', 'grayþe', 'grayþed', 'grayþely', 'grayþez', 'grece', 'gryped', 'grypez', 'grypte', 'gripped', 'gryngolet'],
    'social_exchange':  ['grant', 'grante', 'granted', 'grantez', 'graunt', 'graunte', 'graunted', 'grauntez', 'grome', 'gromez', 'glauer', 'grehoundez', 'gloue', 'glouez']
}

# Dynamically flatten lists into a direct {word: category} mapping
med_map = {word: category for category, words in med_categories.items() for word in words}

# Load data
df = pd.read_csv('sggk_speaker_tokens.csv')
df = df[df['Speaker'] != 'Speaker']
df['Word'] = df['Word'].str.lower()

# Apply mapping
df['semantic_field'] = df['Word'].map(med_map)

df = df.dropna(subset=['semantic_field'])
print(f'\nRetained {len(df)} tokens across {df["semantic_field"].nunique()} semantic fields.')

# Define speaker order (major speakers first)
speaker_order = [s for s in
    ['Narrator', 'Gawain', 'Green Knight', 'Arthur', 'The Lady',
     'Men of the Castle', 'Manservant']
    if s in df['Speaker'].unique()]

table = (
    df.groupby(['Speaker', 'semantic_field'])
    .size()
    .unstack(fill_value=0)
    .reindex(speaker_order)
)

print('Contingency table (token counts):')
print(table.to_string())
print()

# Chi-squared and expected counts
chi2_stat, p, dof, expected = chi2_contingency(table.values)
p_exact = chi2.sf(chi2_stat, dof)

print(f'Chi-squared statistic : {chi2_stat:.4f}')
print(f'Degrees of freedom    : {dof}')
print(f'p-value               : {p_exact:.4f}')
print()

expected_df = pd.DataFrame(expected, index=table.index, columns=table.columns)

# Standardised residuals
residuals = (table.values - expected) / np.sqrt(expected)
residuals_df = pd.DataFrame(residuals, index=table.index, columns=table.columns)
print('Standardised residuals (|r| > 2 = noteworthy):')
print(residuals_df.round(3).to_string())
print()

# Fisher's exact test (per-cell follow-up)
def fisher_test(table_full, target_speaker, field_of_interest):
    tf = table_full.copy()
    target_field   = tf.loc[target_speaker, field_of_interest]
    target_other   = tf.loc[target_speaker].sum() - target_field
    others_field   = tf.drop(index=target_speaker)[field_of_interest].sum()
    others_other   = tf.drop(index=target_speaker).sum().sum() - others_field

    t2 = pd.DataFrame(
        {field_of_interest: [target_field, others_field],
         'other_fields':    [target_other, others_other]},
        index=[target_speaker, 'Other Speakers']
    )
    res = fisher_exact(t2)
    return t2, res

noteworthy = [
    (spk, fld)
    for spk in residuals_df.index
    for fld in residuals_df.columns
    if abs(residuals_df.loc[spk, fld]) > 2
]

for spk, fld in noteworthy:
    t2, res = fisher_test(table, spk, fld)
    sig = '* SIGNIFICANT' if res.pvalue < 0.05 else '(not significant)'
    direction = 'over' if residuals_df.loc[spk, fld] > 0 else 'under'
    print(f'--- {spk} / {fld} ({direction}-represented) ---')
    print(f'  Odds ratio: {res.statistic:.4f}   p-value: {res.pvalue:.5f}  {sig}')