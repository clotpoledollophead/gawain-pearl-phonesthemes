import re
import pandas as pd

def calculate_ttr(filepath, regex_pattern):
    """
    Extracts all words matching the regex pattern from the text,
    and returns the TTR (Types / Tokens), along with the raw counts.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().lower()

    # Find all words matching the specific onset pattern
    matches = re.findall(regex_pattern, text)
    
    if not matches:
        return 0.000
    
    unique_types = set(matches)
    ttr = len(unique_types) / len(matches)
    
    return round(ttr, 3)

files = {'Pearl': 'pearl_cleaned.txt', 'SGGK': 'sggk_cleaned.txt'}

# Define the regex patterns for clusters and sub-clusters
# \b ensures word boundary, \w* captures the rest of the word
patterns = {
    'gl- (overall)': r'\bgl\w*',
    'gr- (overall)': r'\bgr\w*',
    'gri-/gry- sub-cluster': r'\bgr[iy]\w*',
    'grē-/gre- sub-cluster': r'\bgre\w*'
}

# Compile the data into a tabular format
ttr_data = []

for cluster_name, pattern in patterns.items():
    row_data = {'Cluster / sub-cluster': cluster_name}
    for poem_name, filepath in files.items():
        ttr_value = calculate_ttr(filepath, pattern)
        row_data[f'{poem_name} TTR'] = ttr_value
    ttr_data.append(row_data)

# Generate and display the final DataFrame
df_ttr = pd.DataFrame(ttr_data)

print("--- Table 4. Type-Token Ratios ---")
print(df_ttr.to_string(index=False))