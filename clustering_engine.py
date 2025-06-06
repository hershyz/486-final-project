from typing import Dict, List, Set
import tensorflow_hub as hub
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import math
import common

from collections import defaultdict


# hyperparameters for clustering engine
doc_title_weight_factor: float = 1.4                         # significance multiplier the title has over an arbitrary sentence from the rest of the text
cosine_simiarlty_threshold: float = 0.7                      # cosine similarity threshold for adding something to a new cluster
untrusted_cluster_threshold: float = 0.2                     # trustworthiness score threshold for what's determined an untrusted cluster
cluster_keyword_threshold: float = 0.3                       # deviation threshold from p_real = 0.5 for something to be considered a keyword


# parameters for logistic regression classification of clsuters
normalized_cluster_size_weight = 1.8059274235333787
trustworthiness_score_weight = 4.303592006176594
logreg_intercept = -2.219142491933053


# data
embedding = {}                                               # embedding[doc_id] -> 512-dim mean pooled vector embedding
untrusted_clusters = set()                                   # set of untrusted clusters
cluster_keywords: Dict[int, Set[str]] = {}                   # cluster id -> list of keywords
clusters: List[List[int]] = []                               # clusters[i] = [doc id 1, doc id 2, ...]
cluster_trustworthiness: Dict[int, float] = {}               # cluster id -> average probability of a real report [0, 1]
clusters_present: Dict[int, List[int]] = {}                  # doc id -> clusters present in
max_cluster_size: int = 0                                    # running max of the biggest cluster

# load universal sentence encoder
model = hub.load('use_model/archive')


# inference function to predict cluster trustworthiness
def predict_cluster_trustworthiness(cluster_id):
    cluster = clusters[cluster_id]
    
    # compute input features
    normalized_cluster_size = float(len(cluster)) / max_cluster_size
    trustworthiness_score = cluster_trustworthiness[cluster_id]
    
    # logistic regression logit computation
    logit = (
        normalized_cluster_size_weight * normalized_cluster_size +
        trustworthiness_score_weight * trustworthiness_score +
        logreg_intercept
    )
    
    # sigmoid function to convert to probability
    prob_real = 1 / (1 + math.exp(-logit))
    return prob_real


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

    # update cluster keywords
    doc_keywords: Set[str] = set()
    for sentence in sentences:
        for token in common.simple_tokenizer(sentence):
            token_p_real = common.p_real(token)
            if abs(token_p_real - 0.5) >= cluster_keyword_threshold:
                doc_keywords.add(token)

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
    
    # find doc trustworthiness and convert to an indicator variable
    doc_trustworthiness = common.p_real(doc_title + ', ' + doc_text)
    if doc_trustworthiness > 0.5:
        doc_trustworthiness = 1
    else:
        doc_trustworthiness = 0

    # avoid index errors on hashmap
    if doc_id not in clusters_present:
        clusters_present[doc_id] = []

    # add to >=1 clusters
    global max_cluster_size
    if len(clusters_to_add) > 0:

        for cluster_id in clusters_to_add:
            prev_trustworthiness = len(clusters[cluster_id]) * cluster_trustworthiness[cluster_id]
            new_trustworthiness = prev_trustworthiness + doc_trustworthiness
            clusters[cluster_id].append(doc_id)
            new_trustworthiness /= len(clusters[cluster_id])
            cluster_trustworthiness[cluster_id] = new_trustworthiness
            clusters_present[doc_id].append(cluster_id)
            max_cluster_size = max(max_cluster_size, len(clusters[cluster_id]))

        print(f'document {doc_id} assigned to clusters {clusters_to_add}')

    # create a new cluster
    else:

        clusters.append([doc_id])
        cluster_trustworthiness[len(clusters) - 1] = doc_trustworthiness
        clusters_present[doc_id].append(len(clusters) - 1)
        max_cluster_size = max(max_cluster_size, len(clusters[len(clusters) - 1]))

        print(f'new cluster created for document {doc_id}')
    
    # dynamically update inference on untrusted clusters
    if len(clusters_to_add) == 0:
        clusters_to_add.append(len(clusters) - 1)
    for cluster_id in clusters_to_add:
        curr_trustworthiness_score = predict_cluster_trustworthiness(cluster_id)
        if curr_trustworthiness_score <= untrusted_cluster_threshold:
            untrusted_clusters.add(cluster_id)
        elif curr_trustworthiness_score > untrusted_cluster_threshold and cluster_id in untrusted_clusters:
            untrusted_clusters.remove(cluster_id)
    
    # dynamically update cluster keywords
    for cluster_id in clusters_to_add:
        if cluster_id not in cluster_keywords:
                cluster_keywords[cluster_id] = set()
        for keyword in doc_keywords:
            cluster_keywords[cluster_id].add(keyword)

    # all the relevant information needed to return to frontend

    ChangeInCluster = defaultdict(list)
    for docCluster in clusters_to_add:
        # the length of the cluster, the trustworthiness of the cluster, the keywords for the cluster, wehther cluster is untrusted
        ChangeInCluster[docCluster] = [cluster_trustworthiness[docCluster], cluster_keywords[docCluster], True if docCluster in untrusted_clusters else False]

    # Number of documents processed
    return ChangeInCluster

# getter for untrusted clusters
def get_untrusted_clusters() -> List[int]:
    res = list(untrusted_clusters)
    res.sort()
    return res


# getter for cluster keywords
def get_cluster_keywords(cluster_id: int) -> List[int]:
    res = list(cluster_keywords[cluster_id])
    res.sort()
    return res