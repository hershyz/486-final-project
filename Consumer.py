import os
import sys
from dotenv import load_dotenv

from globalFile import Document, Consumer
from clustering_engine import cluster_new

load_dotenv()

testhost = os.getenv("RABBITMQ_HOST")
QueueName = os.getenv("QUEUE_NAME")

print(os.getcwd())

class ConsumerClient():
    def __init__(self):
        print("*" * 20)
        print("Consumer Client Started ...")
        self.consumer = Consumer(testhost, QueueName)
        self.consumer.registerCallback(self.callback)
        self.consumer.startConsumer()

    def callback(self, ch, method, properties, body):

        try:
            document = Document.model_validate_json(body)

            print(f"Processed Document id {document.document_id}")
            cluster_new(document.document_id, document.title, document.content)

        except Exception as e:
            print(e)
            print(f"Document {document.document_id} ran into an error during processing")


# runs consumer
try:
    ConsumerClient()
except KeyboardInterrupt:
    print('\n Consumer shutting down...')
    sys.exit(0)