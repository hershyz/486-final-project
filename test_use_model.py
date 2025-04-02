import tensorflow_hub as hub
import numpy as np
from sklearn.cluster import KMeans

# Load pre-trained Universal Sentence Encoder (USE)
model = hub.load("use_model/archive")

# Sample documents (paragraphs)
documents = [
    "Artificial intelligence is transforming industries with new capabilities.",
    "Machine learning allows computers to learn from data.",
    "Stock prices fluctuate daily due to market forces.",
    "Investing in stocks can lead to long-term financial gains.",
]

# Generate sentence embeddings
embeddings = model(documents)

# Apply K-Means clustering
num_clusters = 2
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
labels = kmeans.fit_predict(embeddings)

# Print cluster assignments
for i, doc in enumerate(documents):
    print(f"Cluster {labels[i]}: {doc}")
