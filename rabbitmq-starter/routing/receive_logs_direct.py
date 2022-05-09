import pika, sys


# Connect to a broker (localhost).
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# exchange - the one responsible for receiving message from the producer and pushing
# that message to the queue.
# direct - the exchange type  when we want to deliver the message
# to the queue bounded by the routing_key
channel.exchange_declare(exchange="direct_logs", exchange_type="direct")


# Let server create a random queue name by passing empty
# string to queue this results to an empty and fresh queue
# whenever we connect to RabbitMQ

# exclusive=True - once the consumer connection is closed, the queue
# should be deleted.
# Generate random queue name with empty queue parameter.
result = channel.queue_declare(queue="", exclusive=True)

# Get the random queue name
queue_name = result.method.queue

# Severity as routing key
severities = sys.argv[1:]

for severity in severities:
    # A. Bind the exchange named 'logs' to queue_name in order for
    # the exchange to send message to this queue
    # B. Bind the routing_key to the queue_name
    channel.queue_bind(exchange="direct_logs", queue=queue_name, routing_key=severity)

# Use this callback to handle incoming messages
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")


# Dispatch message to a consumer/worker that is not busy or
# has already acknowledge its message.
channel.basic_qos(prefetch_count=1)

# Subscribe the callback to `queue_name` queue
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

# Listen for incoming messages
print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
