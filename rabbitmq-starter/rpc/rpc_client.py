import pika
import uuid


class FibonacciRpcClient(object):
    def __init__(self):
        # Setu connection with rabbitMQ
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = self.connection.channel()

        # exclusive=True - once the consumer connection is closed, the queue should be deleted
        # Generate random queue name with empty queue parameter.
        result = self.channel.queue_declare(queue="", exclusive=True)
        self.callback_queue = result.method.queue

        # We want to consume any responses on this queue.
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            # auto_ack - manual acknowledgement is turned on
            auto_ack=True,
        )

    # Response callback
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange="",
            routing_key="rpc_queue",
            properties=pika.BasicProperties(
                # Send reponses to this queue.
                reply_to=self.callback_queue,
                # Tie this id to the response.
                correlation_id=self.corr_id,
            ),
            body=str(n),
        )
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(30)
print(" [.] Got %r" % response)
