import re
import pandas as pd
from collections import Counter

def discover_longest_consonant_clusters(filepath, top_n=15):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    
    # Matches the entire block of initial consonants (including þ and ȝ)
    # until it hits a vowel or non-word character.
    clusters = re.findall(r'\b([^aeiouy\W0-9_]+)', text)
    
    # Filter for clusters of at least 2 letters
    phon_candidates = [c for c in clusters if len(c) >= 2]
    
    return Counter(phon_candidates).most_common(top_n)

def get_precise_counts(filepath, target_list):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    all_words = re.findall(r'\b\w+\b', text)
    
    results = {}
    for phom in target_list:
        # Regex ensures the match is the FULL initial consonant cluster
        # It looks for the cluster followed by a non-consonant (vowel/space/punct)
        pattern = rf'\b{phom}(?![^aeiouy\W0-9_])\w+'
        matches = re.findall(pattern, text)
        
        results[phom] = {
            'count': len(matches),
            'unique_words': set(matches),
            'total_words': len(all_words),
            'instances': matches
        }
    return results

files = ['pearl_cleaned.txt', 'sggk_cleaned.txt']

# Discover top targets dynamically
target_pearl = discover_longest_consonant_clusters(files[0])
target_sggk = discover_longest_consonant_clusters(files[1])
targets_by_file = [[t[0] for t in target_pearl], [t[0] for t in target_sggk]]

# Execute counts
all_data = {f: get_precise_counts(f, t) for f, t in zip(files, targets_by_file)}

# Generate tabular summary
summary = []
for (filename, target_list) in zip(files, targets_by_file):
    data = all_data[filename]
    for p in target_list:
        summary.append({
            'Poem': filename, 
            'Phonestheme': p,
            'Total Occurrences': data[p]['count'],
            'Unique Words': len(data[p]['unique_words']),
            'Density (per 1k words)': round((data[p]['count'] / data[p]['total_words']) * 1000, 2)
        })

df_summary = pd.DataFrame(summary)
print(df_summary)
