import pika

from pydantic import BaseModel

# Document Object constraint checker
class Document(BaseModel):
    document_id: str
    title: str
    content: str


class ConnectionObject:
    def __init__(self, hostName, queueName, port=None):
        self.queueName = queueName
        # self.connection = pika.BlockingConnection(pika.ConnectionParameters(host= hostName))
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=hostName,
                credentials=pika.PlainCredentials('guest', 'guest')
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queueName)

    def __del__(self):
        self.close()

    def close(self):
        if self.connection.is_open:
            self.connection.close()


class Producer(ConnectionObject):
    def __init__(self, hostName, queueName):
        super().__init__(hostName, queueName)

    def __del__(self):
        self.closeProducer()

    def sendDocument(self,jsonDoc):
        self.channel.basic_publish(exchange='', routing_key=self.queueName, body = jsonDoc)

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
        self.channel.start_consuming()

    def closeConsumer(self):
        if self.consumerTag:
            self.channel.basic_cancel(self.consumerTag)
        self.consumerTag = None

        super().close()
