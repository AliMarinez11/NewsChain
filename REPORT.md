# Iteration Report for NewsChain Project

## Overview

This report tracks iterations over the dataset to optimize the clustering and filtering algorithms, aiming to form all 13 expected narratives with high accuracy.

## Iteration 1 - 2025-03-26

**Changes:**

- Switched to Sentence-BERT embeddings for article representations.
- Replaced K-means with hierarchical clustering (distance threshold: 0.3).
- Updated filtering to use Sentence-BERT embeddings (similarity threshold: 0.7, keyword overlap: 0.05).
- Added dynamic title generation using TF-IDF keywords.
- Added evaluation script to compute clustering metrics.

**Results:**

- Narratives Formed: 8/13
- Precision: 0.0000 (incorrect, needs fixing)
- Recall: 0.0000 (incorrect, needs fixing)
- F1-Score: 0.0000 (incorrect, needs fixing)
- Adjusted Rand Index (ARI): 0.2639
- Normalized Mutual Information (NMI): 0.7391

**Observations:**

- Formed 8 narratives: "Tesla Musk", "Walz 2024", "Maher Food", "Trump Tariffs", "Middle East", "Climate Policy", "Supreme Court", "Government Federal" (partial, only tax plan articles).
- Missing 5 narratives: "Ukraine Putin", "Department Education", "Canada State", "Boasberg Judge", "Biden Former" due to articles being split into single-article clusters.
- Hierarchical clustering threshold (0.3) is too strict, resulting in 22 single-article clusters.
- Filtering worked well, with all clusters passing (similarity scores 0.80–0.91).
- Evaluation script has a bug causing incorrect precision, recall, and F1-score.

**Next Steps:**

- Adjust the hierarchical clustering distance threshold (e.g., increase to 0.4) to form larger clusters.
- Fix the evaluation script to handle unclustered articles correctly and compute accurate precision, recall, and F1-score.
- Run the pipeline again and evaluate the results.
