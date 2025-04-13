from typing import Dict, List
import tensorflow_hub as hub
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import common

# hyperparameters
doc_title_weight_factor: float = 1.4                         # significance multiplier the title has over an arbitrary sentence from the rest of the text
cosine_simiarlty_threshold: float = 0.6                      # cosine similarity threshold for adding something to a new cluster

# data
embedding = {}                                               # embedding[doc_id] -> 512-dim mean pooled vector embedding
clusters: List[List[int]] = []                               # clusters[i] = [doc id 1, doc id 2, ...]
cluster_trustworthiness: Dict[int, float] = {}               # cluster id -> average probability of a real report [0, 1]
clusters_present: Dict[int, List[int]] = {}                  # doc id -> clusters present in
n_clustered = 0                                              # number of documents clustered

# load universal sentence encoder
model = hub.load('use_model/archive')

# entry point for a new document, vectorizes the title and the text into a 512-dim vector using mean pooling
def cluster_new(doc_id: int, doc_title: str, doc_text: str):
    
    # create batch embedding job
    sentences = [doc_title]
    for sentence in doc_text.split('.'):
        if sentence.strip():
            sentences.append(sentence)
    
    # generate embeddings from the model and mean pool
    generated_embeddings = model(sentences)

    # generate sentence weights based on how polarized the sentence is (further from 0.5 probability real = higher weight)
    sentence_weights = []
    sentence_weights.append(abs(common.p_real(doc_title) - 0.5) * doc_title_weight_factor)
    sentence_weights = [abs(common.p_real(doc_title) - 0.5) * doc_title_weight_factor] + [
        abs(common.p_real(sentence) - 0.5) for sentence in sentences[1:]
    ]
    sentence_weights = np.array(sentence_weights).reshape(-1, 1)

    # mean pool
    doc_vector = np.sum(generated_embeddings * sentence_weights, axis=0)                                    # weighted sum of sentence vector embeddings
    doc_vector /= np.sum(sentence_weights)                                                                  # document embedding normalization (mean pooling)
    embedding[doc_id] = doc_vector

    # multiclustering + microclustering based on embedding cosine similarity
    clusters_to_add: List[int] = []

    for i, cluster in enumerate(clusters):

        cluster_embeddings = [embedding[doc_id] for doc_id in cluster]
        cluster_centroid = np.mean(cluster_embeddings, axis=0)
        similarity = cosine_similarity([doc_vector], [cluster_centroid])[0][0]

        if similarity >= cosine_simiarlty_threshold:
            clusters_to_add.append(i)
    
    doc_trustworthiness = common.p_real(doc_title + ', ' + doc_text)
    if doc_id not in clusters_present:
        clusters_present[doc_id] = []

    if len(clusters_to_add) > 0:

        for cluster_id in clusters_to_add:
            prev_trustworthiness = len(clusters[cluster_id]) * cluster_trustworthiness[cluster_id]
            new_trustworthiness = prev_trustworthiness + doc_trustworthiness
            clusters[cluster_id].append(doc_id)
            new_trustworthiness /= len(clusters[cluster_id])
            cluster_trustworthiness[cluster_id] = new_trustworthiness
            clusters_present[doc_id].append(cluster_id)

        print(f'document {doc_id} assigned to clusters {clusters_to_add}')

    else:

        clusters.append([doc_id])
        cluster_trustworthiness[len(clusters) - 1] = doc_trustworthiness
        clusters_present[doc_id].append(len(clusters) - 1)

        print(f'new cluster created for document {doc_id}')
    
    # increment number of documents clustered (useful metadata for heuristic)
    global n_clustered
    n_clustered += 1