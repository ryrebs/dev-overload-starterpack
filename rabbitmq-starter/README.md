## Getting started with RabbitMQ

Terms:

A **producer** is a user application that sends messages.

A **queue** is a buffer that stores messages.

A **consumer** is a user application that receives messages.

---

A. **RabbitMQ is a message broker** so it can receive and forward messages.

_Relationship_ - one producer sends message and received by one consumer.

1. Start the receiver with: `python receive.py`

2. Send message to the `hello` queue with: `python send.py`

B. **RabbitMQ as worker queues** - pass time consuming task to multiple workers.

_Relationship_ - one producer sends message and received|processed by one consumer out of the multiple consumers.

- Messages are pass using round robin.
- Prevent message loss when consumer dies by turning on message acknowledgements.
- Make the message survive on restarts and crashes with `durable` option on consumer and `deliver_mode=2` on producer

1. Run multiple workers by running `worker.py` in different terminals

2. Send task with `python new_task.py task`

C. **RabbitMQ as PubSub** - passing all messages not just a subset to multiple consumers is called publish/subscribe.

_Relationship_ - one producer sends message and received by all subscribed consumers.

1. Run consumer 1 `python receive_logs.py`.

2. Run consumer 2 `python receive_logs.py`.

3. Run producer `python emit_log.py`.

C. **Routing** - one producer sends a message to the key goes through a named exchanged determining which queue the message belongs to base on the publish routing key.

_Relationship_ - one producer sends message and routed by a routing_key goes to the queue which is binded to the routing_key. A routing_key key can be binded by one or multiple queue.

1. Run producer for warning and info logs `python emit_log_direct.py warning info "Run. Run. Or it will explode."`.

2. Run producer for error logs `python emit_log_direct.py error "Run. Run. Or it will explode."`.

3. Run consumer for warning `python receive_logs_direct.py warning`.

4. Run consumer for error `python receive_logs_direct.py error`.

D. **Topics** - messages are sent based on matching words in the routing key.

Bindings can be:

\* (star) can substitute for exactly one word.

\# (hash) can substitute for zero or more words.

#### Receive message on 2 Binding keys:

1. Run consumer for binding _\*kern._ and _\*.critical_: `python receive_logs_topic.py "kern.*" "*.critical"`

2. Run producer: `python emit_log_topic.py "kern.asd" "A critical kernel error"`

#### Receive message on all binding keys:

1. Run consumer for binding _#_: `python receive_logs_topic.py "#"`

2. Run producer: `python emit_log_topic.py "any.any" "A critical kernel error"`

#### Receive message on \*.critical binding key:

1. Run consumer for binding _\*.critical_: `python receive_logs_topic.py "*.critical"`

2. Run producer: `python emit_log_topic.py "any.critical" "A critical kernel error"`

#### Receive message on #.critical binding key:

1. Run consumer for binding _#.critical_: `python receive_logs_topic.py "#.critical"`

2. Run producer: `python emit_log_topic.py "any.any.critical" "A critical kernel error"`

E. **RPC** - running a function on a remote computer or Remote Procedure Call.

1. Server: `python rpc_server.py`

2. Client: `python rpc_client.py`

---

Tutorial References are in _https://www.rabbitmq.com/getstarted.html_
