import pandas as pd
import requests
import random

import time
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('data/WELFake_Dataset.csv')

# Endpoint to send POST requests to
POST_URL = "http://localhost:8000/sendDocuments" 

# generator function
def get_random_batches(data, min_batch=1000, max_batch=10000):
    i = 0
    while i < len(data):
        batch_size = random.randint(min_batch, max_batch)
        yield data[i:i+batch_size]
        i += batch_size

documents = [
    {
        "document_id": str(i),
        "title": str(row['title']),
        "content": str(row['text'])
    }
    for i, row in df.iterrows()
]


latencies = []
throughputs = []
batch_sizes = []

# Send in batches
for batch in get_random_batches(documents):
    print(f"Sending batch of {len(batch)} documents...")

    start_time = time.time()

    response = requests.post(
        POST_URL,
        json=batch
    )

    if response.status_code == 200:
        print("✅ Batch sent successfully!")
    else:
        print(f"❌ Failed to send batch: {response.status_code} | {response.text}")

    end_time = time.time()
    duration = end_time - start_time


    latency = duration
    throughput = float(len(batch)) / duration if duration > 0 else 0

    latencies.append(latency)
    throughputs.append(throughput)
    batch_sizes.append(len(batch))

    print(f"✅ Sent in {latency:.2f}s | Throughput: {throughput:.2f} docs/sec")

    time.sleep(random.uniform(1, 5))  # Optional delay between batches



# Plotting
plt.figure(figsize=(12, 5))

# Latency
plt.subplot(1, 2, 1)
plt.plot(latencies, marker='o', label='Latency (s)')
plt.xlabel('Batch #')
plt.ylabel('Latency (s)')
plt.title('Latency per Batch')
plt.grid(True)
plt.legend()

# Throughput
plt.subplot(1, 2, 2)
plt.plot(throughputs, marker='x', color='green', label='Throughput (docs/sec)')
plt.xlabel('Batch #')
plt.ylabel('Throughput')
plt.title('Throughput per Batch')
plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig("latency_throughput_plot.png") 

plt.show()