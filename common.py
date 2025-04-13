import re
import pickle
from typing import List

# simple regex-based tokenizer, keeps contractions
def simple_tokenizer(text: str) -> List[str]:
    tokens = re.findall(r"\b\w+(?:'\w+)?\b", text)
    return tokens

# simple naive bayes inference function, returns the probability [0, 1] that text belongs to a real report
naive_bayes_model = None                             # map of word -> [probability fake, probability real]
def p_real(text: str) -> float:
    global naive_bayes_model
    
    # load naive bayes model into memory if not done so already
    if naive_bayes_model == None:
        with open('naive_bayes_model/naive_bayes_model.pkl', 'rb') as f:
            naive_bayes_model = pickle.load(f)
    
    # fetch probabilities for each token
    probabilities = []
    for token in simple_tokenizer(text):
        if token not in naive_bayes_model:
            probabilities.append(0.5)
        else:
            probabilities.append(naive_bayes_model[token][1])
    
    # return average
    if len(probabilities) == 0:
        return 0.5
    return sum(probabilities) / len(probabilities)