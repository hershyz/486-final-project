# 486-final-project

### Install Dependencies
```bash
pip install tensorflow tensorflow-hub
pip install pandas
pip install scikit-learn
pip install numpy
pip install matplotlib
```

### Download Universal Sentence Encoder Model
```bash
mkdir use_model  # Create a folder for the model
wget https://tfhub.dev/google/universal-sentence-encoder/4?tf-hub-format=compressed -O use_model.tar.gz
tar -xvzf use_model.tar.gz -C use_model  # Extract the model into the folder
```

### Downloading Data
```bash
mkdir data  # Create a folder for the data
```
- Download the file ```WELFake_Dataset.csv``` from [Kaggle](https://www.kaggle.com/datasets/saurabhshahane/fake-news-classification?resource=download).
- Within the CSV, add the feature label ```doc_id``` first on the first line. It should read ```doc_id,title,text,label```.
- Run ```python3 flip_labels.py``` to keep real/fake indexing consistent with the system.

### Building Naive Bayes Model
Run
```bash
python3 train_naive_bayes.py
```
before doing anything further.