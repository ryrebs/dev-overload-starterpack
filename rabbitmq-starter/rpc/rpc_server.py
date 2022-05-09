import pika, sys


# Connect to a broker (localhost).
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()


# Create queue for rpc requests.
result = channel.queue_declare(queue="rpc_queue")

# Function to be called
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


# Request handler
def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    response = fib(n)

    ch.basic_publish(
        exchange="",
        # Reply to is the callback queue. Where responses
        # are sent to.
        routing_key=props.reply_to,
        # correlation_id is an identifier tied to the request.
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str(response),
    )

    # Turn on message acknowledgements
    # to re-deliver all unacknowledge messages.
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Dispatch message to a consumer/worker that is not busy or
# has already acknowledge its message.
channel.basic_qos(prefetch_count=1)

# Subscribe the callback to `rpc_queue` queue
channel.basic_consume(queue="rpc_queue", on_message_callback=on_request)


# Listen for incoming requests
print(" [*] Waiting for requests. To exit press CTRL+C")
channel.start_consuming()
