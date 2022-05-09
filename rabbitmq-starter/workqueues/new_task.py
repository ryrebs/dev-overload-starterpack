import pika, sys


# Connect to a broker (localhost).
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Create the queue where the message should be delivered.
channel.queue_declare(queue="task_queue", durable=True)

# receive message from the command line
message = " ".join(sys.argv[1:]) or "Hello World!"

# Exchange - the one responsible for receiving message from the producer and pushing
# that message to the queue.
# Messages are goes through an "Exchange" before it knows what queue it should belong to.
# We're using a default exchange.
# Your message - body
# Which queue to send - routing_key
channel.basic_publish(
    exchange="",
    routing_key="task_queue",
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    ),
)

# Notify that message was sent
print(f"{message} was sent to.")

# Close the connection and network buffers.
connection.close()
