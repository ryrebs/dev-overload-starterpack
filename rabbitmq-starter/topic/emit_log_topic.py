import pika, sys


# Connect to a broker (localhost).
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# exchange - the one responsible for receiving message from the producer and pushing
# that message to the queue.
# topic - messages are sent based on matching words in the routing key.
channel.exchange_declare(exchange="topic_logs", exchange_type="topic")

# routing_key as topic as routing_key as first parameter
routing_key = sys.argv[1] if len(sys.argv) > 1 else "info"

# create log message from the command line as 2nd parameter
message = " ".join(sys.argv[2:]) or "Hello World!"

# Publish to the named exchange not to a default exchange.
# routing_key value is ignored when using fanout exchange.
channel.basic_publish(exchange="topic_logs", routing_key=routing_key, body=message)


# Notify that message was sent
print(f"{message} was sent to. routing_key {routing_key}")

# Close the connection and network buffers.
connection.close()
