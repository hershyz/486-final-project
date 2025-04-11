import pandas as pd
import os
import pickle
import common

# read dataset into memory
df = pd.read_csv('data/WELFake_Dataset.csv')

# map of word -> [probability fake, probability real]
model = {}

# read all entries
for i, row in df.iterrows():

    doc_title = str(row['title'])
    doc_text = str(row['text'])
    doc_label = int(row['label'])               # true label, 0 for fake, 1 for real

    # run simple tokenizer on doc text
    simple_tokens = common.simple_tokenizer(doc_text)

    # update model with the current tokens
    for token in simple_tokens:
        if token not in model:
            model[token] = [0, 0]
        model[token][doc_label] += 1

# add laplace smoothing
alpha = 1.0
for token in model:
    model[token][0] += alpha
    model[token][1] += alpha

# normalize the model frequencies to convert to probabilities
for token in model:
    n = model[token][0] + model[token][1]
    model[token][0] = float(model[token][0] / n)
    model[token][1] = float(model[token][1] / n)

# display (dump to output file when running to view in entirety)
print('token | P(fake) | P(real)')
for token in model:
    print(token, model[token][0], model[token][1])

# serialize map using pickle module
os.makedirs('naive_bayes_model', exist_ok=True)
with open('naive_bayes_model/naive_bayes_model.pkl', 'wb') as f:
    pickle.dump(model, f)