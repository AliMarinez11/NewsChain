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

## Iteration 2 - 2025-03-27

**Changes:**

- Increased hierarchical clustering distance threshold to 0.4 to form larger clusters.
- Fixed evaluation script to compute accurate precision, recall, and F1-score for clustered articles.

**Results:**

- Narratives Formed: 11/13
- Precision: 0.0000 (still incorrect, needs further debugging)
- Recall: 0.0000 (still incorrect, needs further debugging)
- F1-Score: 0.0000 (still incorrect, needs further debugging)
- Adjusted Rand Index (ARI): 0.3306
- Normalized Mutual Information (NMI): 0.7835

**Observations:**

- Formed 11 narratives: "Ukraine Putin", "Department Education" (partial), "Trump Tariffs" (mixed with Canada State), "Biden Former", "Government Federal", "Tesla Musk", "Supreme Court" (mixed with Boasberg Judge), "Walz 2024", "Maher Food", "Middle East", "Climate Policy".
- Missing 2 narratives: "Boasberg Judge" (mixed in Cluster_0 with Supreme Court articles), "Canada State" (one article in Cluster_4, other in single-article cluster).
- Distance threshold of 0.4 formed larger clusters, recovering "Ukraine Putin" and "Biden Former", but some clusters (e.g., Cluster_0, Cluster_4) are still mixed.
- 11 articles remain in single-article clusters, preventing some narratives from forming fully.
- Evaluation script still producing incorrect precision, recall, and F1-score; needs further debugging.
- Summaries are accurate and focused, but mixed clusters (e.g., Cluster_0, Cluster_4) result in broader summaries.

**Next Steps:**

- Further adjust the hierarchical clustering distance threshold (e.g., try 0.5) to form larger clusters and reduce single-article clusters.
- Debug the evaluation script to compute correct precision, recall, and F1-score metrics.
- Consider refining the filtering step to exclude less cohesive clusters (e.g., lower the keyword overlap threshold).
- Run the pipeline again and evaluate the results.

## Iteration 3 - 2025-03-28

**Changes:**

- Increased hierarchical clustering distance threshold to 0.5 to form larger clusters.
- Skipped summarization to focus on clustering and evaluation.

**Results:**

- Narratives Formed: 11/13
- Precision: 0.0000 (still incorrect, needs further debugging)
- Recall: 0.0000 (still incorrect, needs further debugging)
- F1-Score: 0.0000 (still incorrect, needs further debugging)
- Adjusted Rand Index (ARI): 0.3039
- Normalized Mutual Information (NMI): 0.7575

**Observations:**

- Formed 11 narratives: "Ukraine Putin" (mixed with Middle East), "Department Education" (partial, mixed with Boasberg Judge and Supreme Court), "Trump Tariffs" (mixed with Canada State), "Biden Former", "Government Federal" (split across multiple clusters), "Tesla Musk", "Walz 2024" (mixed with Department Education), "Maher Food", "Middle East" (mixed with Ukraine Putin), "Climate Policy".
- Missing 2 narratives: "Boasberg Judge" (mixed in Cluster_3 with Department Education and Supreme Court), "Canada State" (one article in Cluster_4, other in single-article cluster).
- Distance threshold of 0.5 formed larger clusters, but they’re too broad, mixing unrelated topics (e.g., Cluster_1, Cluster_3).
- 5 articles remain in single-article clusters, preventing some narratives from forming fully.
- Evaluation script still producing incorrect precision, recall, and F1-score; needs further debugging.
- ARI and NMI slightly regressed, indicating decreased clustering quality due to mixed clusters.

**Next Steps:**

- Adjust the hierarchical clustering distance threshold (e.g., try 0.45) to balance between forming larger clusters and avoiding mixed clusters.
- Debug the evaluation script to compute correct precision, recall, and F1-score metrics.
- Tighten the filtering step by lowering the keyword overlap threshold (e.g., from 0.05 to 0.03) to exclude less cohesive clusters.
- Run the pipeline again and evaluate the results.

## Iteration 4 - 2025-03-29

**Changes:**

- Adjusted hierarchical clustering distance threshold to 0.45 to balance cluster size and cohesion.
- Lowered keyword overlap threshold in filtering step to 0.03 to exclude less cohesive clusters.
- Fixed evaluation script to compute correct precision, recall, and F1-score metrics.
- Skipped summarization to focus on clustering and evaluation.

**Results:**

- Narratives Formed: 11/13
- Precision: 0.1111
- Recall: 0.1111
- F1-Score: 0.1111
- Adjusted Rand Index (ARI): 0.3306
- Normalized Mutual Information (NMI): 0.7835

**Observations:**

- Formed 11 narratives: "Ukraine Putin", "Department Education" (partial), "Trump Tariffs" (mixed with Canada State), "Biden Former", "Government Federal" (partial), "Tesla Musk", "Supreme Court" (mixed with Boasberg Judge and Department Education), "Walz 2024", "Maher Food", "Middle East", "Climate Policy".
- Missing 2 narratives: "Boasberg Judge" (mixed in Cluster_0 with Department Education and Supreme Court), "Canada State" (one article in Cluster_4, other in single-article cluster).
- Distance threshold of 0.45 split some mixed clusters (e.g., Ukraine Putin and Middle East are now separate), but Cluster_0 and Cluster_4 are still mixed.
- 11 articles remain in single-article clusters, preventing some narratives from forming fully.
- Lowered keyword overlap threshold (0.03) didn’t exclude any clusters; may need to adjust similarity threshold or further lower keyword overlap.
- Evaluation script now producing correct precision, recall, and F1-score, but scores are very low (0.1111), reflecting mixed clusters.
- ARI and NMI are unchanged, indicating no improvement in clustering quality.

**Next Steps:**

- Adjust the hierarchical clustering distance threshold (e.g., try 0.4) to reduce mixed clusters while maintaining larger clusters.
- Tighten the filtering step by lowering the similarity threshold (e.g., from 0.7 to 0.65) to exclude less cohesive clusters.
- Run the pipeline again and evaluate the results.

## Iteration 5 - 2025-03-30

**Changes:**

- Adjusted hierarchical clustering distance threshold to 0.4 to reduce mixed clusters.
- Lowered similarity threshold in filtering step to 0.65 to exclude less cohesive clusters.
- Skipped summarization to focus on clustering and evaluation.

**Results:**

- Narratives Formed: 11/13
- Precision: 0.1111
- Recall: 0.1111
- F1-Score: 0.1111
- Adjusted Rand Index (ARI): 0.3306
- Normalized Mutual Information (NMI): 0.7835

**Observations:**

- Formed 11 narratives: "Ukraine Putin", "Department Education" (partial), "Trump Tariffs" (mixed with Canada State), "Biden Former", "Government Federal" (partial), "Tesla Musk", "Supreme Court" (mixed with Boasberg Judge and Department Education), "Walz 2024", "Maher Food", "Middle East", "Climate Policy".
- Missing 2 narratives: "Boasberg Judge" (mixed in Cluster_0 with Department Education and Supreme Court), "Canada State" (one article in Cluster_4, other in single-article cluster).
- Distance threshold of 0.4 resulted in the same clustering structure as the previous iteration (0.45), with no improvement in mixed clusters or single-article clusters.
- 11 articles remain in single-article clusters, preventing some narratives from forming fully.
- Lowered similarity threshold (0.65) didn’t exclude any clusters, as those below 0.65 passed due to keyword overlap; need to further tighten filtering criteria.
- Evaluation metrics (precision, recall, F1-score) are unchanged, reflecting the same mixed clusters.
- ARI and NMI are unchanged, indicating no improvement in clustering quality.

**Next Steps:**

- Switch to a different clustering algorithm (e.g., DBSCAN) to better handle varying cluster sizes and reduce single-article clusters.
- Tighten the filtering step by further lowering the keyword overlap threshold (e.g., from 0.03 to 0.01) to exclude less cohesive clusters.
- Run the pipeline again and evaluate the results.
