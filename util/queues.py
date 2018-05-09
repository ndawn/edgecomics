import json

import pika


class Producer:
    def __init__(self, queue):
        self.queue = queue
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)

    def __del__(self):
        self.connection.close()

    def send(self, message):
        if not isinstance(message, str):
            try:
                message = json.dumps(message)
            except TypeError:
                message = str(message)

        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            body=message,
        )
