import os
import sys

import asyncio
import websockets
import threading

from dotenv import load_dotenv
from queue import Queue

from globalFile import Document, Consumer, responseChecker, Producer
from clustering_engine import cluster_new


load_dotenv()

testhost = os.getenv("RABBITMQ_HOST")
QueueName = os.getenv("QUEUE_NAME")


response_queue = Queue()
current_client = None

async def websocket_handler(websocket):
    global current_client
    current_client = websocket
    print("Client connected")

    try:
        await websocket.wait_closed() 
    finally:
        current_client = None
        print("Client disconnected")


async def send_data_to_client():
    while True:
        # wait for new message in a seperate thread without blocking any other tasks
        message = await asyncio.to_thread(response_queue.get)
        if current_client:
            print("Sent message to Client")
            await current_client.send(message)
        
        # confirm task has been completed
        response_queue.task_done()


class ConsumerClient():
    def __init__(self):
        print("*" * 20)
        print("Consumer Client Started ...")
        self.consumer = Consumer(testhost, QueueName)

        self.consumer.registerCallback(self.callback)

    def __call__(self):
        self.consumer.startConsumer()

    def callback(self, ch, method, properties, body):


        try:
            document = Document.model_validate_json(body)

            ClusterChanges = cluster_new(document.document_id, document.title, document.content)
            message = responseChecker(doc=document, ClusterData=ClusterChanges)
            jsonResponse = message.model_dump_json()
            
            print("Sucessfully got data")

            # send data to thread safe queue
            response_queue.put(jsonResponse)
            print(f"Processed Document id {document.document_id}")



        except Exception as e:
            print(e)
            print(f"Document {document.document_id} ran into an error during processing")


async def main():

    server = await websockets.serve(websocket_handler, "localhost", 8080)

    # runs coroutine in the background 
    asyncio.create_task(send_data_to_client())

    # run thread to consume messages
    threading.Thread(target=ConsumerClient()).start()

    # will run for infinite
    await asyncio.Future()
    

# runs consumer
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('\n Consumer shutting down...')
    sys.exit(0)