import json
import numpy as np
from sklearn.metrics import precision_recall_fscore_support, adjusted_rand_score, normalized_mutual_info_score

# Load ground truth
with open('ground_truth.json', 'r') as f:
    ground_truth = json.load(f)

# Load filtered narratives (pipeline output)
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

# Align ground truth and predicted labels, excluding unclustered articles
clustered_articles = list(article_to_predicted_label.keys())
ground_labels = [article_to_ground_label[article] for article in clustered_articles]
predicted_labels = [article_to_predicted_label[article] for article in clustered_articles]

# Compute clustering metrics for clustered articles only
precision, recall, f1, _ = precision_recall_fscore_support(ground_labels, predicted_labels, average='weighted', zero_division=0)
ari = adjusted_rand_score(ground_labels, predicted_labels)
nmi = normalized_mutual_info_score(ground_labels, predicted_labels)

# Compute metrics for all articles (including unclustered ones)
all_articles = list(article_to_ground_label.keys())
all_ground_labels = [article_to_ground_label[article] for article in all_articles]
all_predicted_labels = [article_to_predicted_label.get(article, 'Unclustered') for article in all_articles]
ari_all = adjusted_rand_score(all_ground_labels, all_predicted_labels)
nmi_all = normalized_mutual_info_score(all_ground_labels, all_predicted_labels)

# Print results
print("Metrics for clustered articles only:")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
print("Metrics for all articles (including unclustered):")
print(f"Adjusted Rand Index (ARI): {ari_all:.4f}")
print(f"Normalized Mutual Information (NMI): {nmi_all:.4f}")
print(f"Number of narratives formed: {len(filtered_narratives['validNarratives'])}/13")