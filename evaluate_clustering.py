import json
import numpy as np
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from itertools import combinations

# Load ground truth
with open('ground_truth.json', 'r') as f:
    ground_truth = json.load(f)

# Load filtered narratives (pipeline output after filtering)
with open('filtered_narratives.json', 'r') as f:
    filtered_narratives = json.load(f)

# Create ground truth labels
article_to_ground_label = {}
for article_title, narrative in ground_truth.items():
    article_to_ground_label[article_title] = narrative

# Create predicted labels from filtered narratives
article_to_predicted_label = {}
for cluster_id, cluster_data in filtered_narratives['validNarratives'].items():
    for article in cluster_data['articles']:
        article_title = article['title']
        article_to_predicted_label[article_title] = cluster_id

# Compute pairwise metrics for clustered articles
clustered_articles = list(article_to_predicted_label.keys())
if not clustered_articles:
    print("No articles were clustered.")
    precision, recall, f1 = 0.0, 0.0, 0.0
else:
    # Compute true positives, false positives, and false negatives
    true_positives = 0  # Pairs that are in the same cluster and should be
    false_positives = 0  # Pairs that are in the same cluster but shouldn't be
    false_negatives = 0  # Pairs that should be in the same cluster but aren't

    # Consider all pairs of clustered articles
    for article1, article2 in combinations(clustered_articles, 2):
        ground_same = article_to_ground_label[article1] == article_to_ground_label[article2]
        pred_same = article_to_predicted_label[article1] == article_to_predicted_label[article2]

        if ground_same and pred_same:
            true_positives += 1
        elif not ground_same and pred_same:
            false_positives += 1
        elif ground_same and not pred_same:
            false_negatives += 1

    # Compute total pairs that should be in the same cluster (for recall denominator)
    # We need to consider all articles, including unclustered ones
    all_articles = list(article_to_ground_label.keys())
    ground_clusters = {}
    for article in all_articles:
        label = article_to_ground_label[article]
        if label not in ground_clusters:
            ground_clusters[label] = []
        ground_clusters[label].append(article)

    total_positive_pairs = 0
    for label, articles in ground_clusters.items():
        if len(articles) > 1:
            total_positive_pairs += len(list(combinations(articles, 2)))

    # Compute precision, recall, and F1-score
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / total_positive_pairs if total_positive_pairs > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

# Compute metrics for all articles (including unclustered ones)
all_articles = list(article_to_ground_label.keys())
all_ground_labels = [article_to_ground_label[article] for article in all_articles]
all_predicted_labels = [article_to_predicted_label.get(article, 'Unclustered') for article in all_articles]
ari_all = adjusted_rand_score(all_ground_labels, all_predicted_labels)
nmi_all = normalized_mutual_info_score(all_ground_labels, all_predicted_labels)

# Print results
print("Metrics for clustered articles only (pairwise):")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
print("Metrics for all articles (including unclustered):")
print(f"Adjusted Rand Index (ARI): {ari_all:.4f}")
print(f"Normalized Mutual Information (NMI): {nmi_all:.4f}")
print(f"Number of narratives formed: {len(filtered_narratives['validNarratives'])}/13")

# Print mapping of clusters to ground truth narratives
print("\nCluster to Ground Truth Mapping:")
for cluster_id, cluster_data in filtered_narratives['validNarratives'].items():
    articles = cluster_data['articles']
    ground_narratives = [article_to_ground_label[article['title']] for article in articles]
    most_common_narrative = max(set(ground_narratives), key=ground_narratives.count)
    print(f"{cluster_id} (Title: {cluster_data['generated_title']}) -> {most_common_narrative} ({ground_narratives})")