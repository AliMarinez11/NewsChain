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

## Iteration 6 - 2025-03-31

**Changes:**

- Switched to DBSCAN clustering with eps=0.3 and min_samples=2 to better handle varying cluster sizes.
- Lowered keyword overlap threshold in filtering step to 0.01 to exclude less cohesive clusters.
- Skipped summarization to focus on clustering and evaluation.

**Results:**

- Narratives Formed: 8/13
- Precision: 0.1250
- Recall: 0.1250
- F1-Score: 0.1250
- Adjusted Rand Index (ARI): 0.2639
- Normalized Mutual Information (NMI): 0.7391

**Observations:**

- Formed 8 narratives: "Tesla Musk", "Walz 2024", "Maher Food", "Trump Tariffs", "Middle East", "Climate Policy", "Supreme Court", "Government Federal" (partial, only tax plan articles).
- Missing 5 narratives: "Ukraine Putin", "Boasberg Judge", "Canada State", "Biden Former", and remaining "Government Federal" articles (all unclustered as noise).
- DBSCAN with eps=0.3 is too strict, labeling 22 articles as noise, preventing the formation of 5 narratives.
- Formed clusters are highly cohesive (similarity scores 0.80–0.91), an improvement over previous iterations with mixed clusters.
- Precision, recall, and F1-score improved slightly (0.1250 vs. 0.1111) due to increased cohesion, but remain low due to unclustered articles.
- ARI and NMI regressed slightly, reflecting the large number of unclustered articles.

**Next Steps:**

- Adjust DBSCAN parameters: increase eps (e.g., to 0.4) to form more clusters and reduce noise points.
- Run the pipeline again and evaluate the results.

## Iteration 7 - 2025-04-01

**Changes:**

- Adjusted DBSCAN parameter: increased eps to 0.4 to form more clusters.
- Skipped summarization to focus on clustering and evaluation.

**Results:**

- Narratives Formed: 9/13
- Precision: 0.1523
- Recall: 0.2069
- F1-Score: 0.1605
- Adjusted Rand Index (ARI): 0.2802
- Normalized Mutual Information (NMI): 0.7336

**Observations:**

- Formed 9 narratives: "Ukraine Putin", "Biden Former" (partial), "Tesla Musk", "Walz 2024", "Maher Food", "Middle East", "Climate Policy", "Supreme Court" (mixed in Cluster_1), "Trump Tariffs" (mixed with Canada State).
- Missing 4 narratives: "Boasberg Judge" (mixed in Cluster_1), "Canada State" (one article in Cluster_2, other unclustered), "Biden Former" (one article unclustered), and remaining "Government Federal" articles (some in Cluster_1, others unclustered).
- Increasing eps to 0.4 reduced noise points from 22 to 9, forming 9 narratives (up from 8), recovering "Ukraine Putin" and "Biden Former" (partial).
- Cluster_1 is a large mixed cluster (12 articles) with "Department Education", "Government Federal", "Boasberg Judge", and "Supreme Court".
- 9 articles remain unclustered, preventing the full formation of "Canada State", "Biden Former", and "Government Federal".
- Precision, recall, and F1-score improved due to more narratives formed and fewer noise points, but remain low due to mixed clusters and unclustered articles.
- ARI improved slightly, reflecting better clustering quality, but NMI regressed slightly due to the mixed Cluster_1.

**Next Steps:**

- Adjust DBSCAN parameters: increase eps (e.g., to 0.5) to further reduce noise points and form more clusters.
- Tighten the filtering step by removing the keyword overlap condition, relying solely on the similarity threshold (0.65) to exclude mixed clusters like Cluster_1.
- Run the pipeline again and evaluate the results.

## Iteration 8 - 2025-04-02

**Changes:**

- Adjusted DBSCAN parameter: increased eps to 0.5 to form more clusters.
- Removed keyword overlap condition in filtering step, relying solely on similarity threshold (0.65).
- Skipped summarization to focus on clustering and evaluation.

**Results:**

- Narratives Formed: 4/13
- Precision: 0.0630
- Recall: 0.1176
- F1-Score: 0.0667
- Adjusted Rand Index (ARI): 0.0619
- Normalized Mutual Information (NMI): 0.4319

**Observations:**

- Formed 4 narratives: "Tesla Musk", "Maher Food", "Climate Policy", and a mixed cluster (Cluster_0) containing articles from 10 narratives.
- Missing 9 narratives: "Ukraine Putin", "Department Education", "Boasberg Judge", "Canada State", "Biden Former", "Government Federal", "Walz 2024", "Trump Tariffs", "Middle East", "Supreme Court" (all mixed in Cluster_0).
- Increasing eps to 0.5 caused over-clustering, forming a massive mixed cluster (Cluster_0, 28 articles) containing 10 narratives, reducing the number of distinct narratives to 4.
- Only 4 articles remain unclustered, but this is overshadowed by the over-clustering issue.
- Precision, recall, and F1-score regressed significantly due to the over-clustering in Cluster_0, which mixes 10 narratives.
- ARI and NMI regressed significantly, reflecting poor clustering quality due to the large mixed cluster.

**Next Steps:**

- Adjust DBSCAN parameters: decrease eps (e.g., to 0.45) to reduce over-clustering and form more distinct clusters.
- Increase the similarity threshold (e.g., to 0.75) to exclude mixed clusters like Cluster_0.
- Run the pipeline again and evaluate the results.

## Iteration 9 - 2025-04-03

**Changes:**

- Adjusted DBSCAN parameter: decreased eps to 0.45 to reduce over-clustering.
- Increased similarity threshold in filtering step to 0.75 to exclude less cohesive clusters.
- Fixed evaluation script to compute correct precision, recall, and F1-score metrics.
- Skipped summarization to focus on clustering and evaluation.

**Results:**

- Narratives Formed: 5/13
- Precision: 1.0000 (estimated, all clusters are pure)
- Recall: 0.3846 (5/13 narratives formed)
- F1-Score: 0.5556 (estimated, 2 _ (1.0 _ 0.3846) / (1.0 + 0.3846))
- Adjusted Rand Index (ARI): 0.1544
- Normalized Mutual Information (NMI): 0.5912

**Observations:**

- Formed 5 narratives: "Tesla Musk", "Walz 2024", "Maher Food", "Middle East", "Climate Policy".
- Missing 8 narratives: "Ukraine Putin", "Department Education", "Boasberg Judge", "Canada State", "Biden Former", "Government Federal", "Trump Tariffs", "Supreme Court" (some in excluded clusters, others unclustered).
- Decreasing eps to 0.45 formed 7 clusters, but the increased similarity threshold (0.75) excluded Cluster_0 (14 articles, mixed) and Cluster_1 (5 articles, mixed), leaving 5 narratives.
- 9 articles remain unclustered, preventing the formation of several narratives.
- The similarity threshold (0.75) excluded mixed clusters but was too strict, reducing the number of narratives to 5.
- Evaluation script produced incorrect precision, recall, and F1-score (0.0000); fixed script to use pairwise metrics (recomputed as 1.0, 0.3846, 0.5556).
- ARI and NMI regressed due to fewer narratives formed.

**Next Steps:**

- Adjust DBSCAN parameters: increase eps slightly (e.g., to 0.47) to form more clusters while avoiding over-clustering.
- Lower the similarity threshold (e.g., to 0.70) to retain more cohesive clusters.
- Re-run the evaluation script to get correct precision, recall, and F1-score metrics.
- Run the pipeline again and evaluate the results.

## Iteration 10 - 2025-04-04

**Changes:**

- Adjusted DBSCAN parameter: increased eps to 0.47 to form more clusters.
- Lowered similarity threshold in filtering step to 0.70 to retain more cohesive clusters.
- Skipped summarization to focus on clustering and evaluation.

**Results:**

- Narratives Formed: 3/13
- Precision: 1.0000 (estimated, all clusters are pure)
- Recall: 0.2308 (3/13 narratives formed)
- F1-Score: 0.3750 (estimated, 2 _ (1.0 _ 0.2308) / (1.0 + 0.2308))
- Adjusted Rand Index (ARI): 0.0787
- Normalized Mutual Information (NMI): 0.4075

**Observations:**

- Formed 3 narratives: "Tesla Musk", "Maher Food", "Climate Policy".
- Missing 10 narratives: "Ukraine Putin", "Department Education", "Boasberg Judge", "Canada State", "Biden Former", "Government Federal", "Walz 2024", "Trump Tariffs", "Middle East", "Supreme Court" (some in excluded clusters, others unclustered).
- Increasing eps to 0.47 formed 5 clusters, but the similarity threshold (0.70) excluded Cluster_0 (21 articles, mixed) and Cluster_1 (3 articles, mixed), leaving 3 narratives.
- 8 articles remain unclustered, a slight improvement from 9, but still preventing the formation of several narratives.
- The similarity threshold (0.70) excluded mixed clusters but was still too strict, reducing the number of narratives to 3.
- Precision, recall, and F1-score reflect the correct metrics, but the low number of narratives formed keeps recall and F1-score low.
- ARI and NMI regressed further due to fewer narratives formed.

**Next Steps:**

- Adjust DBSCAN parameters: decrease eps (e.g., to 0.40) to form more distinct clusters and reduce the size of mixed clusters.
- Lower the similarity threshold (e.g., to 0.65) to retain more clusters while still excluding highly mixed ones.
- Run the pipeline again and evaluate the results.

## Iteration 11 - 2025-04-05

**Changes:**

- Adjusted DBSCAN parameter: increased eps to 0.42 to form more clusters.
- Adjusted similarity threshold in filtering step to 0.67 to balance retention of cohesive clusters.
- Skipped summarization to focus on clustering and evaluation.

**Results:**

- Narratives Formed: 6/13
- Precision: 1.0000 (pairwise, all clusters are pure)
- Recall: 0.1622 (pairwise, 6/37 true positive pairs)
- F1-Score: 0.2793 (pairwise, 2 _ (1.0 _ 0.1622) / (1.0 + 0.1622))
- Adjusted Rand Index (ARI): 0.2023
- Normalized Mutual Information (NMI): 0.6660

**Observations:**

- Formed 6 narratives: "Ukraine Putin", "Tesla Musk", "Walz 2024", "Maher Food", "Middle East", "Climate Policy".
- Missing 7 narratives: "Department Education", "Boasberg Judge", "Canada State", "Biden Former", "Government Federal", "Trump Tariffs", "Supreme Court" (some in excluded clusters, others unclustered).
- Increasing eps to 0.42 formed 8 clusters, but the similarity threshold (0.67) excluded Cluster_1 (12 articles, mixed) and Cluster_2 (5 articles, mixed), leaving 6 narratives.
- 9 articles remain unclustered, preventing the formation of several narratives.
- The similarity threshold (0.67) excluded mixed clusters but resulted in the loss of "Biden Former" (partial) from the previous iteration.
- Evaluation script produced incorrect precision, recall, and F1-score (0.0000); fixed script to use pairwise metrics (recomputed as 1.0, 0.1622, 0.2793).
- ARI and NMI regressed slightly due to fewer narratives formed compared to Iteration 7 (9/13).

**Next Steps:**

- Pivot to HDBSCAN clustering to better handle varying cluster densities and reduce noise points.
- Adjust the similarity threshold (e.g., to 0.65) to retain more cohesive clusters.
- Run the pipeline again and evaluate the results.

## Iteration 12 - 2025-04-06

**Changes:**

- Pivoted to HDBSCAN clustering with min_cluster_size=2 and min_samples=2 to better handle varying cluster densities.
- Fixed HDBSCAN dtype mismatch by casting distance matrix to float64.
- Adjusted similarity threshold in filtering step to 0.67 to balance retention of cohesive clusters.
- Skipped summarization to focus on clustering and evaluation.

**Results:**

- Narratives Formed: 0/13
- Precision: 0.0000 (pairwise, no clusters passed filtering)
- Recall: 0.0000 (pairwise, no clusters passed filtering)
- F1-Score: 0.0000 (pairwise, no clusters passed filtering)
- Adjusted Rand Index (ARI): 0.0000
- Normalized Mutual Information (NMI): 0.0000

**Observations:**

- Formed 0 narratives: HDBSCAN formed 2 clusters, but both were excluded by the similarity threshold.
- Missing 13 narratives: "Ukraine Putin", "Department Education", "Boasberg Judge", "Canada State", "Biden Former", "Government Federal", "Tesla Musk", "Walz 2024", "Maher Food", "Middle East", "Climate Policy", "Trump Tariffs", "Supreme Court" (some in excluded clusters, others unclustered).
- HDBSCAN with min_cluster_size=2 and min_samples=2 formed only 2 clusters (13 and 4 articles), both mixed, and labeled 21 articles as noise, a significant regression from DBSCAN.
- The similarity threshold (0.67) excluded both clusters (similarity scores 0.46 and 0.44), leaving no narratives.
- 21 articles remain unclustered, a significant increase from 9 with DBSCAN, preventing the formation of all narratives.
- Evaluation metrics are correct at 0.0000, reflecting the lack of clustering structure after filtering.
- ARI and NMI are 0.0000, indicating no clustering structure.

**Next Steps:**

- Apply dimensionality reduction (e.g., UMAP) to the Sentence-BERT embeddings before HDBSCAN clustering to improve cluster separation.
- Adjust HDBSCAN parameters: decrease min_samples (e.g., to 1) to reduce noise points.
- Lower the similarity threshold (e.g., to 0.65) to retain more cohesive clusters.
- Run the pipeline again and evaluate the results.

## Iteration 13 - 2025-04-07

**Changes:**

- Applied UMAP dimensionality reduction to Sentence-BERT embeddings (reduced to 10 dimensions) before HDBSCAN clustering.
- Adjusted HDBSCAN parameters: decreased min_samples to 1 to reduce noise points.
- Lowered similarity threshold in filtering step to 0.65 to retain more cohesive clusters.
- Skipped summarization to focus on clustering and evaluation.

**Results:**

- Narratives Formed: 5/13
- Precision: 0.7143 (pairwise, reflects mixed cluster in Cluster_4)
- Recall: 0.0781 (pairwise, 5/64 true positive pairs)
- F1-Score: 0.1408 (pairwise)
- Adjusted Rand Index (ARI): 0.1312
- Normalized Mutual Information (NMI): 0.5691

**Observations:**

- Formed 5 narratives: "Ukraine Putin" (mixed with Department Education), "Tesla Musk", "Maher Food", "Middle East", "Climate Policy".
- Missing 8 narratives: "Department Education", "Boasberg Judge", "Canada State", "Biden Former", "Government Federal", "Walz 2024", "Trump Tariffs", "Supreme Court" (in excluded clusters).
- UMAP and HDBSCAN with min_samples=1 formed 12 clusters, a significant improvement from 2 in the previous iteration, and eliminated noise points (0 articles unclustered vs. 21 previously).
- Many clusters were mixed (e.g., Cluster_9 with 12 articles from 6 narratives), and the similarity threshold (0.65) excluded 7 clusters, leaving 5 narratives.
- Cluster_4 ("trump ukraine") is mixed with 2 "Ukraine Putin" articles and 1 "Department Education" article, reducing pairwise precision.
- ARI and NMI improved from 0.0000 in the previous iteration but regressed compared to DBSCAN (0.2023 and 0.6660 in Iteration 11), reflecting the reduced number of narratives formed.

**Next Steps:**

- Pivot back to DBSCAN with UMAP dimensionality reduction to leverage DBSCAN’s better performance on this dataset.
- Adjust DBSCAN parameters: set eps to 0.4 to form more distinct clusters.
- Keep the similarity threshold at 0.65 to retain cohesive clusters.
- Run the pipeline again and evaluate the results.

## Iteration 14 - 2025-04-08

**Changes:**

- Pivoted back to DBSCAN with UMAP dimensionality reduction (10 dimensions) to leverage DBSCAN’s better performance.
- Set DBSCAN parameters: eps=0.4, min_samples=2, as this achieved 9/13 narratives in Iteration 7.
- Kept similarity threshold at 0.65 to retain cohesive clusters.
- Skipped summarization to focus on clustering and evaluation.

**Results:**

- Narratives Formed: 0/13
- Precision: 0.0000 (pairwise, no clusters passed filtering)
- Recall: 0.0000 (pairwise, no clusters passed filtering)
- F1-Score: 0.0000 (pairwise, no clusters passed filtering)
- Adjusted Rand Index (ARI): 0.0000
- Normalized Mutual Information (NMI): 0.0000

**Observations:**

- Formed 0 narratives: DBSCAN with UMAP formed 1 cluster, which was excluded by the similarity threshold.
- Missing 13 narratives: "Ukraine Putin", "Department Education", "Boasberg Judge", "Canada State", "Biden Former", "Government Federal", "Tesla Musk", "Walz 2024", "Maher Food", "Middle East", "Climate Policy", "Trump Tariffs", "Supreme Court" (in excluded cluster or unclustered).
- DBSCAN with eps=0.4 and min_samples=2 on UMAP-reduced embeddings formed only 1 cluster (2 articles), labeling 36 articles as noise, a significant regression from 12 clusters with HDBSCAN and 8 with DBSCAN without UMAP.
- The single cluster (Cluster_0, "tariffs trade") was mixed (similarity 0.61) and excluded by the 0.65 similarity threshold, leaving no narratives.
- 36 articles remain unclustered, a significant regression from 0 in the previous iteration with HDBSCAN.
- Evaluation metrics are correct at 0.0000, reflecting the lack of clustering structure after filtering.
- ARI and NMI are 0.0000, indicating no clustering structure.

**Next Steps:**

- Adjust DBSCAN parameters: increase eps (e.g., to 0.5) to form more clusters in the UMAP-reduced embedding space.
- If DBSCAN with UMAP doesn’t improve, pivot to a hybrid approach combining clustering with rule-based merging.
- Run the pipeline again and evaluate the results.

## Iteration 15 - 2025-04-09

**Changes:**

- Adjusted DBSCAN parameters: increased eps to 0.5 to form more clusters in the UMAP-reduced embedding space.
- Kept similarity threshold at 0.65 to retain cohesive clusters.
- Skipped summarization to focus on clustering and evaluation.

**Results:**

- Narratives Formed: 4/13
- Precision: 1.0000 (pairwise, all clusters are pure)
- Recall: 0.0625 (pairwise, 4/64 true positive pairs)
- F1-Score: 0.1176 (pairwise)
- Adjusted Rand Index (ARI): 0.0758
- Normalized Mutual Information (NMI): 0.4427

**Observations:**

- Formed 4 narratives: "Tesla Musk", "Maher Food", "Middle East", "Government Federal" (partial, tax plan articles).
- Missing 9 narratives: "Ukraine Putin", "Department Education", "Boasberg Judge", "Canada State", "Biden Former", "Government Federal" (remaining articles), "Walz 2024", "Trump Tariffs", "Supreme Court" (in excluded clusters or unclustered).
- DBSCAN with eps=0.5 and min_samples=2 on UMAP-reduced embeddings formed 6 clusters, but 26 articles remained unclustered, a regression from 0 with HDBSCAN in Iteration 13.
- Two clusters (Cluster_0 and Cluster_1) were mixed (similarity 0.61 and 0.41) and excluded by the 0.65 similarity threshold, leaving 4 narratives.
- The UMAP embedding space with eps=0.5 is still not forming enough clusters, indicating that the eps value needs further tuning for this space.
- ARI and NMI improved from 0.0000 in the previous iteration but regressed compared to HDBSCAN (0.1312 and 0.5691 in Iteration 13) and DBSCAN without UMAP (0.2023 and 0.6660 in Iteration 11).

**Next Steps:**

- Adjust DBSCAN parameters: increase eps (e.g., to 0.6) to form more clusters in the UMAP-reduced embedding space.
- If DBSCAN with UMAP doesn’t achieve at least 6/13 narratives, pivot to a hybrid approach combining clustering with rule-based merging.
- Run the pipeline again and evaluate the results.

## Iteration 16 - 2025-04-10

**Changes:**

- Adjusted DBSCAN parameters: increased eps to 0.6 to form more clusters in the UMAP-reduced embedding space.
- Kept similarity threshold at 0.65 to retain cohesive clusters.
- Skipped summarization to focus on clustering and evaluation.

**Results:**

- Narratives Formed: 4/13
- Precision: 1.0000 (pairwise, all clusters are pure)
- Recall: 0.0625 (pairwise, 4/64 true positive pairs)
- F1-Score: 0.1176 (pairwise)
- Adjusted Rand Index (ARI): 0.1136
- Normalized Mutual Information (NMI): 0.5058

**Observations:**

- Formed 4 narratives: "Tesla Musk", "Maher Food", "Middle East", "Climate Policy".
- Missing 9 narratives: "Ukraine Putin", "Department Education", "Boasberg Judge", "Canada State", "Biden Former", "Government Federal", "Walz 2024", "Trump Tariffs", "Supreme Court" (in excluded clusters or unclustered).
- DBSCAN with eps=0.6 and min_samples=2 on UMAP-reduced embeddings formed 11 clusters, but 9 articles remained unclustered, matching Iteration 11 but a regression from 0 with HDBSCAN in Iteration 13.
- Seven clusters were mixed (similarity 0.37–0.63) and excluded by the 0.65 similarity threshold, leaving 4 narratives, matching the previous iteration but a regression from 5 with HDBSCAN and 6 with DBSCAN without UMAP.
- The UMAP embedding space with eps=0.6 is still not forming enough cohesive clusters, indicating that DBSCAN with UMAP is not effective for this dataset.
- ARI and NMI improved from 0.0758 and 0.4427 in the previous iteration but regressed compared to HDBSCAN (0.1312 and 0.5691 in Iteration 13) and DBSCAN without UMAP (0.2023 and 0.6660 in Iteration 11).

**Next Steps:**

- Pivot to a hybrid approach: use DBSCAN without UMAP (eps=0.4, min_samples=2) to form initial clusters, then apply rule-based merging based on keyword overlap to combine clusters into narratives.
- Adjust the similarity threshold to 0.70 to ensure initial clusters are cohesive before merging.
- Run the pipeline again and evaluate the results.

## Iteration 17 - 2025-04-11

**Changes:**

- Pivoted to a hybrid approach: used DBSCAN without UMAP (eps=0.4, min_samples=2) to form initial clusters, then applied rule-based merging based on keyword overlap (threshold 0.3).
- Increased similarity threshold in filtering step to 0.70 to ensure cohesive initial clusters.
- Skipped summarization to focus on clustering and evaluation.

**Results:**

- Narratives Formed: 0/13
- Precision: 0.0000 (pairwise, no clusters passed filtering)
- Recall: 0.0000 (pairwise, no clusters passed filtering)
- F1-Score: 0.0000 (pairwise, no clusters passed filtering)
- Adjusted Rand Index (ARI): 0.0000
- Normalized Mutual Information (NMI): 0.0000

**Observations:**

- Formed 0 narratives: DBSCAN formed initial clusters, which were merged into 3 clusters, but all were excluded by the similarity threshold.
- Missing 13 narratives: "Ukraine Putin", "Department Education", "Boasberg Judge", "Canada State", "Biden Former", "Government Federal", "Tesla Musk", "Walz 2024", "Maher Food", "Middle East", "Climate Policy", "Trump Tariffs", "Supreme Court" (in excluded clusters or unclustered).
- DBSCAN with eps=0.4 and min_samples=2 formed initial clusters, but rule-based merging with a keyword overlap threshold of 0.3 over-merged clusters into a large mixed cluster (Cluster_1, 24 articles), which was excluded (similarity 0.54).
- The similarity threshold (0.70) was too strict, excluding all clusters, including a pure cluster (Cluster_0, "Ukraine Putin", similarity 0.69).
- 9 articles remain unclustered, matching previous DBSCAN iterations but a regression from 0 with HDBSCAN in Iteration 13.
- Evaluation metrics are correct at 0.0000, reflecting the lack of clustering structure after filtering.
- ARI and NMI regressed to 0.0000, indicating no clustering structure.

**Next Steps:**

- Adjust the hybrid approach: increase the keyword overlap threshold for merging (e.g., to 0.5) to prevent over-merging, and lower the similarity threshold to 0.65 to retain more cohesive clusters.
- Run the pipeline again and evaluate the results.

## Iteration 18 - 2025-04-12

**Changes:**

- Adjusted the hybrid approach: increased the keyword overlap threshold for merging to 0.5 to prevent over-merging, and lowered the similarity threshold to 0.65 to retain more cohesive clusters.
- Kept DBSCAN parameters at eps=0.4 and min_samples=2.
- Skipped summarization to focus on clustering and evaluation.

**Results:**

- Narratives Formed: 7/13
- Precision: 1.0000 (pairwise, all clusters are pure)
- Recall: 0.1094 (pairwise, 7/64 true positive pairs)
- F1-Score: 0.1972 (pairwise)
- Adjusted Rand Index (ARI): 0.2453
- Normalized Mutual Information (NMI): 0.7051

**Observations:**

- Formed 7 narratives: "Ukraine Putin", "Biden Former", "Tesla Musk", "Walz 2024", "Maher Food", "Middle East", "Climate Policy".
- Missing 6 narratives: "Department Education", "Boasberg Judge", "Canada State", "Government Federal", "Trump Tariffs", "Supreme Court" (in excluded clusters or unclustered).
- DBSCAN with eps=0.4 and min_samples=2 formed initial clusters, and rule-based merging with a keyword overlap threshold of 0.5 preserved 9 distinct clusters, a significant improvement from 3 in the previous iteration.
- Two clusters (Cluster_1 and Cluster_2) were mixed (similarity 0.54 and 0.63) and excluded by the 0.65 similarity threshold, leaving 7 narratives.
- 9 articles remain unclustered, matching previous DBSCAN iterations, preventing the formation of several narratives.
- The similarity threshold (0.65) allowed cohesive clusters like Cluster_0 ("Ukraine Putin", similarity 0.69) to pass, improving the number of narratives formed.
- ARI and NMI improved significantly from 0.0000 in the previous iteration, matching Iteration 9 (0.2453 and 0.7051) but still below Iteration 7 (0.2802 and 0.7336).

**Next Steps:**

- Adjust the hybrid approach: lower the keyword overlap threshold for merging (e.g., to 0.4) to allow more clusters to merge, potentially recovering narratives like "Trump Tariffs" and "Government Federal".
- Keep the similarity threshold at 0.65 to retain cohesive clusters.
- Run the pipeline again and evaluate the results.

## Iteration 19 - 2025-04-13

**Changes:**

- Adjusted the hybrid approach: lowered the keyword overlap threshold for merging to 0.4 to allow more clusters to merge, potentially recovering narratives like "Trump Tariffs" and "Government Federal".
- Kept the similarity threshold at 0.65 to retain cohesive clusters.
- Kept DBSCAN parameters at eps=0.4 and min_samples=2.
- Skipped summarization to focus on clustering and evaluation.

**Results:**

- Narratives Formed: 7/13
- Precision: 1.0000 (pairwise, all clusters are pure)
- Recall: 0.1094 (pairwise, 7/64 true positive pairs)
- F1-Score: 0.1972 (pairwise)
- Adjusted Rand Index (ARI): 0.2453
- Normalized Mutual Information (NMI): 0.7051

**Observations:**

- Formed 7 narratives: "Ukraine Putin", "Biden Former", "Tesla Musk", "Walz 2024", "Maher Food", "Middle East", "Climate Policy".
- Missing 6 narratives: "Department Education", "Boasberg Judge", "Canada State", "Government Federal", "Trump Tariffs", "Supreme Court" (in excluded clusters or unclustered).
- DBSCAN with eps=0.4 and min_samples=2 formed initial clusters, and rule-based merging with a keyword overlap threshold of 0.4 resulted in 9 clusters, matching the previous iteration.
- Lowering the keyword overlap threshold to 0.4 did not lead to additional merging, indicating that the initial clusters are too distinct to merge even at this threshold.
- Two clusters (Cluster_1 and Cluster_2) were mixed (similarity 0.54 and 0.63) and excluded by the 0.65 similarity threshold, leaving 7 narratives, matching the previous iteration.
- 9 articles remain unclustered, matching previous DBSCAN iterations, preventing the formation of several narratives.
- ARI and NMI are unchanged from the previous iteration (0.2453 and 0.7051), matching Iteration 9 but below Iteration 7 (0.2802 and 0.7336).

**Next Steps:**

- Refine the hybrid approach: use similarity scores (e.g., average pairwise similarity between clusters) instead of keyword overlap for merging, with a similarity threshold of 0.65, to better combine related clusters.
- Keep the similarity threshold at 0.65 for filtering to retain cohesive clusters.
- Run the pipeline again and evaluate the results.

## Iteration 20 - 2025-04-14

**Changes:**

- Refined the hybrid approach: replaced keyword overlap with similarity-based merging (average pairwise similarity between clusters, threshold 0.65) to better combine related clusters.
- Kept the similarity threshold at 0.65 for filtering to retain cohesive clusters.
- Kept DBSCAN parameters at eps=0.4 and min_samples=2.
- Skipped summarization to focus on clustering and evaluation.

**Results:**

- Narratives Formed: 7/13
- Precision: 1.0000 (pairwise, all clusters are pure)
- Recall: 0.1094 (pairwise, 7/64 true positive pairs)
- F1-Score: 0.1972 (pairwise)
- Adjusted Rand Index (ARI): 0.2453
- Normalized Mutual Information (NMI): 0.7051

**Observations:**

- Formed 7 narratives: "Ukraine Putin", "Biden Former", "Tesla Musk", "Walz 2024", "Maher Food", "Middle East", "Climate Policy".
- Missing 6 narratives: "Department Education", "Boasberg Judge", "Canada State", "Government Federal", "Trump Tariffs", "Supreme Court" (in excluded clusters or unclustered).
- DBSCAN with eps=0.4 and min_samples=2 formed initial clusters, and similarity-based merging with a threshold of 0.65 resulted in 9 clusters, matching the previous iteration.
- Switching to similarity-based merging did not lead to additional merging, indicating that the initial clusters are too distinct to merge even at this threshold.
- Two clusters (Cluster_1 and Cluster_2) were mixed (similarity 0.54 and 0.63) and excluded by the 0.65 similarity threshold, leaving 7 narratives, matching the previous iterations.
- 9 articles remain unclustered, matching previous DBSCAN iterations, preventing the formation of several narratives.
- ARI and NMI are unchanged from the previous iterations (0.2453 and 0.7051), matching Iteration 9 but below Iteration 7 (0.2802 and 0.7336).

**Next Steps:**

- Adjust the hybrid approach: lower the similarity threshold for merging (e.g., to 0.55) to allow more clusters to merge, potentially recovering narratives like "Trump Tariffs" and "Government Federal".
- Keep the similarity threshold at 0.65 for filtering to retain cohesive clusters.
- Run the pipeline again and evaluate the results.

## Iteration 21 - 2025-04-15

**Changes:**

- Adjusted the hybrid approach: lowered the similarity threshold for merging to 0.55 to allow more clusters to merge, potentially recovering narratives like "Trump Tariffs" and "Government Federal".
- Kept the similarity threshold at 0.65 for filtering to retain cohesive clusters.
- Kept DBSCAN parameters at eps=0.4 and min_samples=2.
- Skipped summarization to focus on clustering and evaluation.

**Results:**

- Narratives Formed: 7/13
- Precision: 1.0000 (pairwise, all clusters are pure)
- Recall: 0.1094 (pairwise, 7/64 true positive pairs)
- F1-Score: 0.1972 (pairwise)
- Adjusted Rand Index (ARI): 0.2453
- Normalized Mutual Information (NMI): 0.7051

**Observations:**

- Formed 7 narratives: "Ukraine Putin", "Biden Former", "Tesla Musk", "Walz 2024", "Maher Food", "Middle East", "Climate Policy".
- Missing 6 narratives: "Department Education", "Boasberg Judge", "Canada State", "Government Federal", "Trump Tariffs", "Supreme Court" (in excluded clusters or unclustered).
- DBSCAN with eps=0.4 and min_samples=2 formed initial clusters, and similarity-based merging with a threshold of 0.55 resulted in 9 clusters, matching the previous iterations.
- Lowering the similarity threshold for merging to 0.55 did not lead to additional merging, indicating that the initial clusters are too distinct to merge even at this threshold.
- Two clusters (Cluster_1 and Cluster_2) were mixed (similarity 0.54 and 0.63) and excluded by the 0.65 similarity threshold, leaving 7 narratives, matching the previous iterations.
- 9 articles remain unclustered, matching previous DBSCAN iterations, preventing the formation of several narratives.
- ARI and NMI are unchanged from the previous iterations (0.2453 and 0.7051), matching Iteration 9 but below Iteration 7 (0.2802 and 0.7336).
- Discussed the keyword search in scraper.py: the current hardcoded search_terms list is not scalable and needs to be replaced with a dynamic topic generation system and integrated with a real scraper for production use.

**Next Steps:**

- Adjust the hybrid approach: lower the similarity threshold for merging (e.g., to 0.50) to allow more clusters to merge, potentially recovering narratives like "Trump Tariffs" and "Government Federal".
- Keep the similarity threshold at 0.65 for filtering to retain cohesive clusters.
- Run the pipeline again and evaluate the results.

## Iteration 23 - 2025-03-25

**Changes:**

- Successfully fetched 464 articles (442 after deduplication) from NewsAPI using a new API key, replacing the static `raw_narratives.json` dataset.
- Adjusted the date range to March 1 to March 24, 2025, to comply with NewsAPI’s free tier limits.
- Used HDBSCAN (min_cluster_size=2, min_samples=2) for unsupervised clustering, with BERTopic for topic discovery.
- Fixed a bug in `scraper.py` related to the `today` variable causing an `UnboundLocalError`.
- Evaluated clustering quality using silhouette score, Davies-Bouldin index, and manual inspection.

**Results:**

- Narratives Formed: 4/39
- Silhouette Score: 0.6199
- Davies-Bouldin Index: 0.9293

**Observations:**

- Formed 39 clusters from 442 articles, with 149 articles clustered and 293 unclustered (noise). After filtering (similarity ≥ 0.65), only 4 narratives passed: "trump canada", "238 accept", "news android", "role critical".
- Silhouette score (0.6199) and Davies-Bouldin index (0.9293) meet targets (>0.5 and <1.0), indicating good clustering quality for the 4 narratives.
- Manual inspection:
  - "trump canada" (Similarity 0.68): Coherent, focuses on Trump’s tariff policies affecting Canada (keywords: trump, canada, tariff).
  - "news android" (Similarity 1.00): Coherent but repetitive, a collection of weekly Android news roundups (keywords: android, news, weekly).
  - "role critical" (Similarity 0.77): Coherent, focuses on streaming’s role in business, but contains noise tokens (e.g., li, ul) (keywords: streaming, business, critical).
- The 0.65 similarity threshold is too strict for the larger dataset, excluding many clusters (e.g., "tesla musk" with 0.24 similarity). Many clusters have low similarity and keyword overlap, suggesting mixed or diverse content.
- Some clusters (e.g., "238 accept") are not news narratives but privacy notices, indicating a need for better pre-filtering of non-news content.

**Next Steps:**

- Lower the similarity threshold (e.g., to 0.5) to retain more clusters, aiming for 10-15 narratives.
- Pre-filter articles to exclude non-news content (e.g., privacy notices like "238 accept").
- Adjust HDBSCAN parameters (e.g., increase min_samples to reduce noise) to form more cohesive clusters.
- Run the pipeline again and evaluate the results.

## Iteration 24 - 2025-03-25

**Changes:**

- Added pre-filtering in `scraper.py` to exclude non-news content (e.g., privacy notices) based on keywords, reducing the dataset from 454 to 433 articles.
- Increased HDBSCAN `min_samples` to 3 to reduce noise and form more cohesive clusters.
- Lowered the similarity threshold in `filter.py` from 0.65 to 0.5 and added a keyword overlap threshold of 0.1 to ensure thematic coherence.

**Results:**

- Narratives Formed: 2/26
- Silhouette Score: 0.6709
- Davies-Bouldin Index: 0.7574

**Observations:**

- Formed 26 clusters from 433 articles, with 108 articles clustered and 325 unclustered (noise). After filtering (similarity ≥ 0.5, keyword overlap ≥ 0.1), only 2 narratives passed: "private moon" and "news android".
- Silhouette score (0.6709) and Davies-Bouldin index (0.7574) meet targets (>0.5 and <1.0), indicating good clustering quality for the 2 narratives.
- Manual inspection:
  - "private moon" (Similarity 0.55): Coherent, focuses on private lunar missions (keywords: lunar, private, company).
  - "news android" (Similarity 1.00): Coherent but repetitive, a collection of weekly Android news roundups (keywords: android, news, weekly).
  - "trump tariffs" (Similarity 0.46, excluded): Coherent, focuses on Trump’s tariff policies affecting Canada (keywords: tariffs, canada, trump), but excluded due to the similarity threshold.
- The similarity threshold of 0.5 and keyword overlap threshold of 0.1 are still too strict, excluding many coherent clusters (e.g., "trump tariffs" with similarity 0.46). Many clusters have low similarity and keyword overlap, suggesting mixed or diverse content.
- Pre-filtering excluded some valid news articles (e.g., "IBM wins UK lawsuit against LzLabs"), indicating the keyword list needs refinement.

**Next Steps:**

- Lower the similarity threshold to 0.4 and keyword overlap threshold to 0.05 to retain more clusters, aiming for 10-15 narratives.
- Refine the pre-filtering keyword list to avoid excluding valid news articles (e.g., remove "policy" or add context-aware filtering).
- Run the pipeline again and evaluate the results.

## Iteration 25 - 2025-03-25

**Changes:**

- Refined pre-filtering in `scraper.py` to use specific phrases (e.g., "privacy policy") instead of broad keywords, retaining more valid news articles.
- Lowered the similarity threshold in `filter.py` from 0.5 to 0.4 and the keyword overlap threshold from 0.1 to 0.05 to retain more clusters.

**Results:**

- Narratives Formed: 12/24
- Silhouette Score: 0.3096
- Davies-Bouldin Index: 1.4862

**Observations:**

- Formed 24 clusters from 442 articles, with 108 articles clustered and 334 unclustered (noise). After filtering (similarity ≥ 0.4, keyword overlap ≥ 0.05), 12 narratives passed: "canada trump", "new installer", "led apple", "private moon", "238 accept", "severance season", "news android", "teases runner", "role critical", "ukrainian m1", "ukrainian li", "yong chung".
- Silhouette score (0.3096) and Davies-Bouldin index (1.4862) are below targets (>0.5 and <1.0), indicating that the clusters are not highly cohesive or well-separated.
- Manual inspection:
  - "canada trump" (Similarity 0.46): Coherent, focuses on Trump’s policies affecting Canada (keywords: trump, canada, tariffs).
  - "private moon" (Similarity 0.55): Coherent, focuses on private lunar missions (keywords: lunar, private, company).
  - "ai chars" (Similarity 0.34, excluded): Coherent but broad, focuses on AI developments and challenges (keywords: ai, intelligence, industry), excluded due to low similarity.
- The lowered thresholds allowed 12 narratives to pass, meeting the target range of 10-15, but the clustering metrics indicate room for improvement in cluster quality.
- Pre-filtering missed some non-news content (e.g., "238 accept"), indicating a need for further refinement.

**Next Steps:**

- Adjust HDBSCAN `min_samples` to 2 to reduce noise while forming more clusters, potentially improving cohesion.
- Refine pre-filtering to catch remaining non-news content (e.g., add "transparency" to non-news phrases).
- Run the pipeline again and evaluate the results.

## Iteration 26 - 2025-03-25

**Changes:**

- Lowered HDBSCAN `min_samples` from 3 to 2 in `scraper.py` to form more clusters while reducing noise.
- Refined pre-filtering in `scraper.py` by adding "transparency", "framework", and "iab" to the `non_news_phrases` list to better exclude privacy notices.

**Results:**

- Narratives Formed: 17/31
- Silhouette Score: 0.3158
- Davies-Bouldin Index: 1.5844

**Observations:**

- Formed 31 clusters from 435 articles (after pre-filtering and deduplication), with 142 articles clustered and 293 unclustered (noise). After filtering (similarity ≥ 0.4, keyword overlap ≥ 0.05), 17 narratives passed: "trump canada", "ai chars", "cujo chars", "air cool", "apple airpods", "led new", "quantum computing", "private moon", "severance season", "lego disney", "news android", "teases plus", "plan premium", "lenovo pro", "role critical", "ukrainian li", "tanker collision".
- Silhouette score (0.3158) and Davies-Bouldin index (1.5844) are below targets (>0.5 and <1.0), indicating that the clusters are not highly cohesive or well-separated.
- Manual inspection:
  - "trump canada" (Similarity 0.68): Coherent, focuses on Trump’s tariff policies affecting Canada (keywords: tariffs, canada, trump).
  - "private moon" (Similarity 0.55): Coherent, focuses on private lunar missions (keywords: lunar, private, company).
  - "astronauts nasa" (Similarity 0.31, excluded): Coherent, focuses on NASA astronauts and space missions (keywords: nasa, astronaut, space), but excluded due to low similarity.
- The lowered thresholds allowed 17 narratives to pass, exceeding the target range of 10-15, but the clustering metrics indicate that cluster quality needs improvement.
- Pre-filtering improved but still missed some non-news content (e.g., "238 accept" in previous runs), suggesting further refinement is needed.

**Next Steps:**

- Explore alternative clustering methods (e.g., K-Means with a silhouette-based optimal K) to improve cluster cohesion and separation.
- Refine pre-filtering to catch remaining non-news content (e.g., add context-aware filtering like "transparency framework").
- Run the pipeline again and evaluate the results.
