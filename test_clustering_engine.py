import pandas as pd
import matplotlib.pyplot as plt
import collections
import clustering_engine

# randomly sample n rows
df = pd.read_csv('data/WELFake_Dataset.csv')
n = 1000                                        # change this to however many samples we want to test the clustering engine with
sampled_df = df.sample(n=n)

# display what we sampled and invoke the clustering engine
for doc_id, row in sampled_df.iterrows():

    doc_title = str(row['title'])
    doc_text = str(row['text'])
    doc_label = int(row['label'])

    if len(doc_title) == 0 or len(doc_text) == 0 or doc_label == None:
        continue
    
    print(f'doc_id: {doc_id}')
    print(f'doc_title: {doc_title}')
    print(f'doc_label {doc_label}')

    clustering_engine.cluster_new(doc_id=doc_id, doc_title=doc_title, doc_text=doc_text)

    print("-" * 50)

for _ in range(25):
    print('~')

# display clusters by doc titles
for i, cluster in enumerate(clustering_engine.clusters):
    print(f'Cluster {i}:')
    for doc_id in cluster:
        doc_title = sampled_df.loc[doc_id, 'title']
        print(f"  - {doc_title}")

    print("-" * 50)

# visualize
cluster_sizes = [len(cluster) for cluster in clustering_engine.clusters]
# cluster_size_counts = collections.Counter(cluster_sizes)
# sizes = sorted(cluster_size_counts.keys())  
# frequencies = [cluster_size_counts[size] for size in sizes]
# plt.figure(figsize=(24, 12))
# plt.bar(sizes, frequencies, color='skyblue', edgecolor='black')
# plt.xlabel('Cluster Size')
# plt.ylabel('Frequency')
# plt.title('Distribution of Cluster Sizes')
# plt.xticks(sizes, rotation=90)  # Show all sizes clearly
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.show()
plt.figure(figsize=(12, 6))

# Use a histogram with automatic binning for better visualization
plt.hist(cluster_sizes, bins=range(1, max(cluster_sizes) + 2), color='skyblue', edgecolor='black', alpha=0.7)

plt.xlabel('Cluster Size')
plt.ylabel('Frequency')
plt.title('Distribution of Cluster Sizes')

# Adjust x-axis ticks to be readable
plt.xticks(rotation=45)

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
