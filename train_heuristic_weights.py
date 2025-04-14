import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import clustering_engine

# settings
n = 10000                           # number of documents to sample (10x clustering engine test)
real_report_ratio = 0.75            # ratio of real reports to use (same as clustering engine test)
n_cluster_threshold = 1000          # stop generating data once these many clusters have been created

# randomly sample reports
df = pd.read_csv('data/WELFake_Dataset.csv')
real_df = df[df['label'] == 1]
fake_df = df[df['label'] == 0]
real_n = int(n * real_report_ratio)
fake_n = n - real_n
sampled_real = real_df.sample(n=real_n, replace=False)
sampled_fake = fake_df.sample(n=fake_n, replace=False)
sampled_df = pd.concat([sampled_real, sampled_fake]).sample(frac=1).reset_index(drop=True)

# invoke clustering engine
real_docs = set()
fake_docs = set()
for i, row in sampled_df.iterrows():

    doc_id = int(row['doc_id'])
    doc_title = str(row['title'])
    doc_text = str(row['text'])
    doc_label = int(row['label'])

    if doc_label == 1:
        real_docs.add(doc_id)
    else:
        fake_docs.add(doc_id)
    
    clustering_engine.cluster_new(doc_id=doc_id, doc_title=doc_title, doc_text=doc_text)

    # early stopping
    if len(clustering_engine.clusters) >= n_cluster_threshold:
        break

# generate dataframe for training
rows = []
for cluster_id in range(len(clustering_engine.clusters)):
    cluster = clustering_engine.clusters[cluster_id]

    # get input features
    normalized_cluster_size = float(len(cluster)) / clustering_engine.max_cluster_size
    cluster_trustworthiness_score = clustering_engine.cluster_trustworthiness[cluster_id]
    
    # determine output feature
    real_ratio = sum(1 for doc_id in cluster if doc_id in real_docs)
    real_ratio = float(real_ratio) / len(cluster)
    output_feature: int = 0
    if real_ratio > 0.5:
        output_feature = 1
    
    # append to training data
    rows.append({
        'normalized_cluster_size': normalized_cluster_size,
        'trustworthiness_score': cluster_trustworthiness_score,
        'label': output_feature
    })

# train logistic regression
cluster_training_df = pd.DataFrame(rows)
X = cluster_training_df[['normalized_cluster_size', 'trustworthiness_score']]
y = cluster_training_df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
classifier = LogisticRegression()
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

for _ in range(25):
    print('~')
print(f'logreg accuracy: {accuracy * 100:.2f}%')
print(f'Weight for normalized_cluster_size: {classifier.coef_[0][0]}')
print(f'Weight for trustworthiness_score: {classifier.coef_[0][1]}')
print(f'Intercept: {classifier.intercept_[0]}')

'''
    logreg accuracy: 96.00%
    Weight for normalized_cluster_size: 1.8059274235333787
    Weight for trustworthiness_score: 4.303592006176594
    Intercept: -2.219142491933053
'''