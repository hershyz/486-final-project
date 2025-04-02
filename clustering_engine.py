import tensorflow_hub as hub
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# hyperparameters
doc_title_weight_factor: int = 2                             # significance multiplier the title has over an arbitrary sentence from the rest of the text
mean_simiilarity_threshold: float = 0.5                      # discriminating cosine silimarity threshold for creating a new cluster

# data
embedding = {}                                               # embedding[doc_id] -> 512-dim mean pooled vector embedding
clusters = []                                                # clusters[i] = [doc id 1, doc id 2, ...]

# load universal sentence encoder
model = hub.load('use_model/archive')

# entry point for a new document, vectorizes the title and the text into a 512-dim vector using mean pooling
def cluster_new(doc_id: int, doc_title: str, doc_text: str):
    
    # # create batch embedding job
    sentences = []
    for _ in range(doc_title_weight_factor):
        sentences.append(doc_title)
    for sentence in doc_text.split('.'):
        if sentence.strip():
            sentences.append(sentence)
    
    # generate embeddings from the model and mean pool
    generated_embeddings = model(sentences)
    doc_vector = np.mean(generated_embeddings, axis=0)
    embedding[doc_id] = doc_vector

    # microcluster based on embedding
    # best_mean_similarity = starting_best_mean_similarity         # best cosine similarity to a cluster to beat
    # best_cluster = None                                          # index of the best cluster

    # for i, cluster in enumerate(clusters):
        
    #     cluster_embeddings = [embedding[doc_id] for doc_id in cluster]
    #     cluster_centroid = np.mean(cluster_embeddings, axis=0)
    #     similarity = cosine_similarity([doc_vector], [cluster_centroid])[0][0]

    #     if abs(similarity) > abs(best_mean_similarity):
    #         best_mean_similarity = similarity
    #         best_cluster = i
        
    # if best_cluster is not None:
    #     clusters[best_cluster].append(doc_id)
    # else:
    #     clusters.append([doc_id])
    
    # print(f'document {doc_id} assigned to cluster {best_cluster} with similarity {best_mean_similarity}.')

    matched_clusters = []
    for i, cluster in enumerate(clusters):
        
        cluster_embeddings = [embedding[doc_id] for doc_id in cluster]
        cluster_centroid = np.mean(cluster_embeddings, axis=0)
        similarity = cosine_similarity([doc_vector], [cluster_centroid])[0][0]

        if abs(similarity) > mean_simiilarity_threshold:
            matched_clusters.append(i)
        
    if len(matched_clusters) == 0:
        clusters.append([doc_id])
    else:
        for match_id in matched_clusters:
            clusters[match_id].append(doc_id)
    
    print(f'document {doc_id} assigned to clusters {matched_clusters}.')