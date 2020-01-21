import pika
import sys
import pytest


@pytest.mark.usefixture('connect_to_rabbit', 'messages_number')
def test_publisher(connect_to_rabbit, messages_number):
    channel = connect_to_rabbit
    channel.exchange_declare(exchange='direct_exchange', exchange_type='direct')
    q = channel.queue_declare(queue='test_queue', durable=True)
    channel.queue_bind(exchange='direct_exchange', queue="test_queue", routing_key="direct.routing.key")

    message = " ".join(sys.argv[1:]) or "Hello World!"

    channel.confirm_delivery()
    try:
        for i in range(int(messages_number)):
            channel.basic_publish(exchange='direct_exchange', body=message, routing_key="direct.routing.key")
    except pika.exceptions.UnroutableError:
        print("Failed to send message %r" % message)

    assert q.method.message_count == 50
    channel.close()
