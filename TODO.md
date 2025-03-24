# TODO for NewsChain Project

## Current Goal

Optimize the clustering and filtering logic to achieve near-perfect accuracy, ensuring all 13 narratives are formed consistently with high-quality summaries. Focus on using the best tools and techniques available, even if they require learning, to build a robust foundation before moving to scaling, HTML, or other features.

## Tasks

### 1. Ground Truth Dataset

- [x] Create a labeled ground truth dataset (`ground_truth.json`) mapping the 38 articles to their correct 13 narratives.
- [ ] Confirm the ground truth mapping with the user and make any necessary adjustments.

### 2. Upgrade to Better Article Representations

- [ ] Install the `sentence-transformers` library (`pip install sentence-transformers`).
- [ ] Update `scraper.py` to use Sentence-BERT embeddings (e.g., `all-MiniLM-L6-v2` model) instead of TF-IDF for article representations.
- [ ] Test the new embeddings to ensure they work with the current dataset.

### 3. Switch to Hierarchical Clustering

- [ ] Update `scraper.py` to replace K-means with hierarchical clustering (agglomerative clustering) using cosine similarity on Sentence-BERT embeddings.
- [ ] Implement a distance threshold for clustering to form cohesive clusters dynamically, rather than specifying a fixed number of clusters.
- [ ] Remove the current post-clustering refinement step, as hierarchical clustering should handle this implicitly.

### 4. Automate Evaluation with Clustering Metrics

- [ ] Write a new script (`evaluate_clustering.py`) to compute clustering metrics (precision, recall, F1-score, Adjusted Rand Index, Normalized Mutual Information) by comparing the pipeline’s output to the ground truth.
- [ ] Integrate the evaluation script into the pipeline to run automatically after clustering and filtering.

### 5. Refine Filtering Logic

- [ ] Update `filter.py` to use Sentence-BERT embeddings for computing similarity between articles, replacing the current TF-IDF-based approach.
- [ ] Adjust the filtering thresholds (similarity and keyword overlap) to work with the new embeddings, ensuring valid narratives are not excluded.

### 6. Test and Iterate

- [ ] Run the updated pipeline with the new clustering, embeddings, and filtering logic.
- [ ] Evaluate the results using the clustering metrics script, aiming to achieve all 13 narratives with high accuracy (e.g., F1-score > 0.9).
- [ ] Iterate by adjusting parameters (e.g., distance threshold for hierarchical clustering, filtering thresholds) based on the metrics until the target is met.

### 7. Final Validation

- [ ] Run the pipeline one final time and manually inspect the summaries to ensure they are focused and accurate.
- [ ] Confirm that all 13 narratives are formed consistently with no unrelated articles in the clusters.
- [ ] Save the final version to GitHub as the optimized baseline.

### Future Steps (After Logic Optimization)

- Integrate a news API for real-time scraping.
- Scale the pipeline to handle larger datasets.
- Enhance the HTML frontend for better user experience.
- Explore advanced NLP techniques (e.g., fine-tuned BERT, topic modeling) with funding and a team.

## Notes

- Prioritize accuracy over speed, as we’re not in a rush.
- Use the best tools available (e.g., Sentence-BERT, hierarchical clustering) to ensure robust logic.
- The current version (10 narratives) is saved to GitHub as a working baseline.
