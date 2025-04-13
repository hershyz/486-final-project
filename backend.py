import os
import uvicorn

from fastapi import FastAPI
from typing import List, Union
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# custom class imports

from globalFile import Document, Producer


@asynccontextmanager
async def lifespan(app: FastAPI):
    # persistent channel connection and declaration and connection of channel
    load_dotenv()

    testhost = os.getenv("RABBITMQ_HOST")
    app.state.QueueName = os.getenv("QUEUE_NAME")

    app.state.producer = Producer(testhost, app.state.QueueName)

    print("Server is starting up...")

    yield

    app.state.producer.closeProducer()
    print("Connection closed and Sever is shutting down...")


# fastAPI object
app = FastAPI(lifespan=lifespan)



@app.post("/sendDocuments")
async def submit_documents(docs: Union[Document, List[Document]]):
    if isinstance(docs, Document): 
        docs = [docs]

    for doc in docs:
        # Note could make seperate file for producer but its like a one line command
        try:
            jsonDoc = doc.model_dump_json()
            app.state.producer.sendDocument(jsonDoc)
            print(f"Succesfully published {doc.document_id} to queue {app.state.QueueName}")
            
        except Exception as e:
            print(f"ERROR: {e}")
            print(f"ERROR: Failed to publish {doc.document_id} to queue {app.state.QueueName}")




# backend must be run manually - single instance right now
if __name__ == "__main__":
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)