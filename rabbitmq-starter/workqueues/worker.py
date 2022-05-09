import pika, os, sys, time


def main():
    # Connect to a broker (localhost).
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Create the queue where the message should be delivered.
    # Idempotent declaration - doesn't matter how many times
    # we execute 'queue_declare' it will return the same result.
    # We make sure queue exists before receiving messages.
    # So we need to declare it again.
    # Durable = true - to make the messages survive when RabbitMQ crashes and restart
    channel.queue_declare(queue="task_queue", durable=True)

    # Use this callback to handle incoming messages
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        print(f" [x] Received decoded body {body.decode()}")
        print(f" [x] Done in {body.count(b'')}")

        # Fake long task
        time.sleep(body.count(b""))
        print("Done")

        # Turn on message acknowledgements
        # to re-deliver all unacknowledge messages.
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Dispatch message to a consumer/worker that is not busy or
    # has already acknowledge its message.
    channel.basic_qos(prefetch_count=1)

    # Subscribe the callback to `task_queue` queue
    channel.basic_consume(queue="task_queue", on_message_callback=callback)

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
