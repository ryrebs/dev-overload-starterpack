import pika

# Connect to a broker (localhost).
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Create the queue where the message should be delivered.
channel.queue_declare(queue="hello")


# Messages are goes through an "Exchange" before it knows what queue it should belong to.
# We're using a default exchange.
# Your message - routing_key
# Which queue to send - body
channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")


# Close the connection and network buffers.
connection.close()
