import pika, os, sys


def main():
    # Connect to a broker (localhost).
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Create the queue where the message should be delivered.
    # Idempotent declaration - doesn't matter how many times
    # we execute 'queue_declare' it will return the same result.
    # We make sure queue exists before receiving messages.
    # So we need to declare it again.
    channel.queue_declare(queue="hello")

    # Use this callback to handle incoming messages
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    # Subscribe the callback to `hello` queue
    # auto_ack - manual acknowledgement is turned on
    channel.basic_consume(queue="hello", auto_ack=True, on_message_callback=callback)

    # Listen for incoming messages
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
