import os
import re
from bs4 import BeautifulSoup

def clean_poem_html(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"File {input_file} not found. Skipping.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    line_spans = soup.find_all('span', class_='line')
    
    cleaned_lines = []
    for span in line_spans:
        for milestone in span.find_all('span', class_='milestone--span'):
            milestone.decompose()
        
        line_text = span.get_text().strip()
        if line_text:
            cleaned_lines.append(line_text)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_lines))
    print(f"Successfully cleaned '{input_file}' -> '{output_file}'")

files_to_process = {'pearl.html': 'pearl_cleaned.txt', 'sggk.html': 'sggk_cleaned.txt'}
for html_file, txt_file in files_to_process.items():
    clean_poem_html(html_file, txt_file)
