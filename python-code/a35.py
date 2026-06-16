import re
import pandas as pd
from scipy.stats import chi2_contingency

def count_vowel_subclusters(filepath, consonant_cluster):
    """
    Extracts words starting with the target consonant cluster and 
    categorizes them by the immediately following orthographic vowel.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().lower()

    # Regex matches the cluster boundary and captures the next vowel
    pattern = rf'\b{consonant_cluster}([aeioy])\w*'
    matches = re.findall(pattern, text)

    # Initialize count dictionary (merging i and y orthographies)
    counts = {'a': 0, 'e': 0, 'i_y': 0, 'o': 0}
    
    for vowel in matches:
        if vowel in ['i', 'y']:
            counts['i_y'] += 1
        elif vowel in counts:
            counts[vowel] += 1

    # Return as an ordered list for the contingency table
    return [counts['a'], counts['e'], counts['i_y'], counts['o']]

# Define files and target clusters
files = {'Pearl': 'pearl_cleaned.txt', 'SGGK': 'sggk_cleaned.txt'}
clusters = ['gl', 'gr']

# Execute analysis for each poem
for poem_name, filepath in files.items():
    contingency_table = []
    
    # Build 2x4 table: [[gl_a, gl_e, gl_i/y, gl_o], [gr_a, gr_e, gr_i/y, gr_o]]
    for cl in clusters:
        contingency_table.append(count_vowel_subclusters(filepath, cl))

    # Apply Pearson Chi-Squared Test
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)

    # Output formatting
    print(f"--- {poem_name} Internal Vowel Chi-Squared Analysis ---")
    print(f"gl- counts [a, e, i/y, o]: {contingency_table[0]}")
    print(f"gr- counts [a, e, i/y, o]: {contingency_table[1]}")
    print(f"Chi-squared (X^2) = {chi2:.3f}")
    print(f"p-value = {p_value:.3f}")
    print(f"Degrees of freedom = {dof}\n")