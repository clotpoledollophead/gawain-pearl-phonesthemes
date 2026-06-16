# Pearl-Poet Phonesthemes: A Computational Analysis of *gl-* and *gr-*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

Replication data, semantic lexicons, and Python scripts for the computational stylometric analysis of the *gl-* and *gr-* phonesthemes in *Pearl* and *Sir Gawain and the Green Knight* (Cotton Nero A.x). 

This repository contains the full data pipeline utilized to map the sonic architecture of the poems, featuring Kolmogorov-Smirnov distribution tests, temporal mapping, and speaker-stratified contingency analyses.

## Repository Structure

The repository is divided into reproducible datasets and the Python codebase used for statistical testing and visualization.

* **`datasets/`**
  * **`html/`**: Raw source files (`pearl.html`, `sggk.html`) extracted from the digital transcripts.
  * **`txt/`**: Cleaned, line-delimited plain text files (`pearl_cleaned.txt`, `sggk_cleaned.txt`). *Note: The SGGK file retains the diplomatic reading of the closing French motto (Total lines: 2531).*
  * **`csv/`**: Intermediate structured data bridging the raw texts and statistical outputs (e.g., `speaker_tokens.csv`, `sggk_speaker_tokens.csv`).
  * **`json/`**: Custom, MED-based semantic lexicons (`pearl_gl_gr_lexicon.json`, `sggk_gl_gr_lexicon.json`) used to map Middle English vocabulary to semantic fields.
* **`python-code/`**: The Python scripts (`.py`) used to parse the corpora, execute Fisher's Exact and Chi-Squared tests, calculate Type-Token Ratios (TTR), and generate cumulative distribution functions (CDFs).
* **`output-figures/`**: High-resolution generated charts (e.g., `figure_1_normalized_density.png`, `figure_2_ks_ecdf.png`).

## Prerequisites and Replication

To reproduce the statistical findings and visual charts, ensure you have Python 3.8+ installed along with the following standard data science libraries:

`pip install pandas numpy scipy matplotlib seaborn beautifulsoup4 wordcloud`

To run the pipeline, execute the scripts located in the `python-code/` directory. The scripts are designed to ingest the raw texts from the `datasets/txt/` and `datasets/json/` folders and output the resulting terminal statistics and `.png` figures.

## Dual License

To encourage open science and reproducibility in the digital humanities, this repository utilizes a dual-licensing structure:

* **Source Code:** All Python scripts (`.py` files) in the `python-code/` directory are released under the [MIT License](LICENSE).
* **Datasets & Lexicons:** All data files, including the cleaned text corpora (`.txt`), structured data (`.csv`), and semantic lexicons (`.json`), are released under a [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You are free to share and adapt the data, provided appropriate credit is given.

## Citation

If you utilize this methodology, codebase, or semantic lexicon in your own research, please cite the corresponding conference presentation:

> Lee, Hsin-Ying. (2026). *‘Gawain’ or ‘Gawain’t’: Quantifying the Ambiguous Salvation and Authorship in Sir Gawain and the Green Knight*. Paper presented at the 2026 International Conference of the Taiwan Association of Classical, Medieval and Renaissance Studies (TACMRS). Arete Honors Program, National Yang Ming Chiao Tung University.

```
