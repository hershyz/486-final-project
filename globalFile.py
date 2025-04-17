import pika

from pydantic import BaseModel
from typing import Dict, List, Any


# Document Object constraint checker
class Document(BaseModel):
    document_id: str
    title: str
    content: str

class responseChecker(BaseModel):
    doc: Document
    ClusterData: Dict[int, list[Any]]




class ConnectionObject:
    def __init__(self, hostName, queueName, port=None):
        self.queueName = queueName
        self.hostName = hostName
        self.connection = None
        self.channel = None
        self.reconnect()
        # self.connection = pika.BlockingConnection(pika.ConnectionParameters(host= hostName))
       

    def __del__(self):
        self.close()


    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()

    def reconnect(self):
            self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.hostName,
                credentials=pika.PlainCredentials('guest', 'guest'),
                heartbeat=600 # 10 minute heartbeat
                )
            )
        
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queueName)



class Producer(ConnectionObject):
    def __init__(self, hostName, queueName):
        self.hostname = hostName
        self.queueName = queueName
        super().__init__(hostName, queueName)

    def __del__(self):
        self.closeProducer()

    def sendDocument(self,jsonDoc):
        try:
            self.channel.basic_publish(exchange='', routing_key=self.queueName, body = jsonDoc)
        except Exception as e:
            self.reconnect()

    def closeProducer(self):
        super().close()


class Consumer(ConnectionObject):
    def __init__(self, hostName, queueName):
        super().__init__(hostName, queueName)
        self.consumerTag = None

    def __del__(self):
        self.closeConsumer()


    def registerCallback(self,callbackFunction):
        if self.consumerTag:
            self.channel.basic_cancel(self.consumerTag)
        
        self.consumerTag = self.channel.basic_consume(queue=self.queueName, on_message_callback=callbackFunction, auto_ack=True)


    def startConsumer(self):
        while True:
            try:
                self.channel.start_consuming()
            except Exception as e:
                print("Regaining Connection")
                self.reconnect()

    def closeConsumer(self):
        if self.consumerTag:
            self.channel.basic_cancel(self.consumerTag)
        self.consumerTag = None

        super().close()
