# 486-final-project

### 1) Install Dependencies
```bash
pip install tensorflow tensorflow-hub
pip install pandas
pip install scikit-learn
pip install numpy
pip install matplotlib
```

### 2) Download Universal Sentence Encoder Model
```bash
mkdir use_model  # Create a folder for the model
wget https://tfhub.dev/google/universal-sentence-encoder/4?tf-hub-format=compressed -O use_model.tar.gz
# Extract, move `archive` into the `use_model` directory
```

### 3) Download Dataset
```bash
mkdir data  # Create a folder for the data
```
- Download the file ```WELFake_Dataset.csv``` from [Kaggle](https://www.kaggle.com/datasets/saurabhshahane/fake-news-classification?resource=download).
- Within the CSV, add the feature label ```doc_id``` first on the first line. It should read ```doc_id,title,text,label```.
- Run ```python3 flip_labels.py``` to keep real/fake indexing consistent with the system.

### 4) Train Naive Bayes Model
Run
```bash
python3 train_naive_bayes.py
```
<<<<<<< Updated upstream
=======
before doing anything further.

## RabbitMQ on Docker
Run the following commands to create a rabbitMQ container

```bash
docker pull rabbitmq:3
docker run -d --name rabbitmq -p 5672:5672 rabbitmq:3
```

## Running the backend
Open terminal and run the following command from the root directory

```bash
python3 backend.py
```

## Running Consumer Endpoints
Open terminal and run the following command from the root directory

``` bash
python3 Consumer.py
```

- TODO : After pipeline, combine the backend docker and Consumer into a shell script so it can be run very simply with configurable arguments
>>>>>>> Stashed changes
