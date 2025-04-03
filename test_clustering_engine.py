import pandas as pd
import matplotlib.pyplot as plt
import time
import clustering_engine

# hyperparameters
n = 1000                           # number of sampled reports (without replacement)
real_report_ratio = 0.75           # ratio of real reports to use

# randomly sample reports
df = pd.read_csv('data/WELFake_Dataset.csv')
# sampled_df = df.sample(n=n)
real_df = df[df['label'] == 1]
fake_df = df[df['label'] == 0]
real_n = int(n * real_report_ratio)
fake_n = n - real_n
sampled_real = real_df.sample(n=real_n, replace=False)
sampled_fake = fake_df.sample(n=fake_n, replace=False)
sampled_df = pd.concat([sampled_real, sampled_fake]).sample(frac=1).reset_index(drop=True)

# display what we sampled and invoke the clustering engine
real_docs = set()
fake_docs = set()
clustering_latencies = []
num_clustered_docs = []
for i, row in sampled_df.iterrows():

    doc_id = int(row['doc_id'])
    doc_title = str(row['title'])
    doc_text = str(row['text'])
    doc_label = int(row['label'])

    if doc_label == 1:
        real_docs.add(doc_id)
    else:
        fake_docs.add(doc_id)

    if len(doc_title) == 0 or len(doc_text) == 0 or doc_label == None:
        continue
    
    print(f'doc_id: {doc_id}')
    print(f'doc_title: {doc_title}')
    print(f'doc_label {doc_label}')

    start_time = time.time()
    clustering_engine.cluster_new(doc_id=doc_id, doc_title=doc_title, doc_text=doc_text)
    end_time = time.time()

    clustering_latencies.append(end_time - start_time)
    num_clustered_docs.append(i)

    print("-" * 50)

for _ in range(25):
    print('~')

# display clusters by doc titles
for i, cluster in enumerate(clustering_engine.clusters):
    print(f'Cluster {i}:')
    for doc_id in cluster:
        # doc_title = sampled_df.loc[doc_id, 'title']
        doc_title = sampled_df[sampled_df['doc_id'] == doc_id]['title'].values[0]
        print(f"  - {doc_title}")

    print("-" * 50)

# visualize cluster sizes and their frequency of occurrence
cluster_sizes = [len(cluster) for cluster in clustering_engine.clusters]
plt.figure(figsize=(12, 6))
plt.hist(cluster_sizes, bins=range(1, max(cluster_sizes) + 2), color='skyblue', edgecolor='black', alpha=0.7)
plt.xlabel('Cluster Size')
plt.ylabel('Frequency')
plt.title('Distribution of Cluster Sizes')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# visualize correlation between cluster size and ratio of real documents
cluster_sizes = []
real_ratios = []

for cluster in clustering_engine.clusters:
    cluster_size = len(cluster)
    num_real = sum(1 for doc_id in cluster if doc_id in real_docs)
    num_fake = cluster_size - num_real

    real_ratio = num_real / cluster_size if cluster_size > 0 else 0

    cluster_sizes.append(cluster_size)
    real_ratios.append(real_ratio)

plt.figure(figsize=(10, 6))
plt.scatter(cluster_sizes, real_ratios, alpha=0.6, color='blue', edgecolors='black')
plt.xlim(0, 100)
plt.ylim(0, 1)
plt.xlabel('Cluster Size')
plt.ylabel('Real Report Ratio')
plt.title('Correlation Between Cluster Size and Real Report Ratio')
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

# visualize clustering latencies
plt.figure(figsize=(10, 6))
plt.plot(num_clustered_docs, clustering_latencies, marker='o', linestyle='-', color='red', alpha=0.7)
plt.xlabel('Number of Documents Clustered')
plt.ylabel('Time to Cluster (seconds)')
plt.title('Clustering Time vs. Number of Documents Clustered')
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()
