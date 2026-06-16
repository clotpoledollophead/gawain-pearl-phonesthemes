import re
import pandas as pd
from collections import Counter

CONSONANTS = set('bcdfghjklmnpqrstvwxyz')
MIN_COUNT  = 10

def extract_all_clusters(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    words = re.findall(r'\b[a-z]+\b', text)
    counts, examples = Counter(), {}
    
    for w in words:
        i = 0
        while i < len(w) and w[i] in CONSONANTS:
            i += 1
        cluster = w[:i]
        if len(cluster) >= 2:  # Isolate clusters of 2+ consonants
            counts[cluster] += 1
            examples.setdefault(cluster, set()).add(w)
            
    return counts, examples, len(words)

# Process both files
p_counts, p_words, p_total = extract_all_clusters('pearl_cleaned.txt')
s_counts, s_words, s_total = extract_all_clusters('sggk_cleaned.txt')

# Filter for exclusivity
rows = []
for cl in sorted(set(p_counts) | set(s_counts)):
    p, s = p_counts.get(cl, 0), s_counts.get(cl, 0)
    
    if p >= MIN_COUNT and s == 0:
        rows.append({'Cluster': cl + '-', 'Exclusive to': 'Pearl',
                     'Count': p, 'Density (per 1k words)': round(p/p_total*1000, 2),
                     'Top examples': ', '.join(sorted(p_words[cl])[:5])})
                     
    elif s >= MIN_COUNT and p == 0:
        rows.append({'Cluster': cl + '-', 'Exclusive to': 'SGGK',
                     'Count': s, 'Density (per 1k words)': round(s/s_total*1000, 2),
                     'Top examples': ', '.join(sorted(s_words[cl])[:5])})

# Format and display output
df_table2 = (pd.DataFrame(rows)
               .sort_values(['Exclusive to', 'Count'], ascending=[True, False])
               .reset_index(drop=True))

print(f"Poem-Exclusive Clusters (≥{MIN_COUNT} tokens in home poem, 0 in other)")
print(df_table2)