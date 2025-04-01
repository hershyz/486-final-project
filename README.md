# 486-final-project

### Install Dependencies
```bash
pip install tensorflow tensorflow-hub
```

### Download Universal Sentence Encoder Model
```bash
mkdir use_model  # Create a folder for the model
wget https://tfhub.dev/google/universal-sentence-encoder/4?tf-hub-format=compressed -O use_model.tar.gz
tar -xvzf use_model.tar.gz -C use_model  # Extract the model into the folder
```