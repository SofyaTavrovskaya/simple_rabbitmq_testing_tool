import pika
import pytest


@pytest.mark.usefixture('connect_to_rabbit', 'messages_number')
def test_publisher(connect_to_rabbit, messages_number):
    channel = connect_to_rabbit
    message = "Hello World!"
    channel.confirm_delivery()
    for i in range(messages_number):
        channel.basic_publish(exchange='test_exchange', routing_key='direct.routing.key',
                              body=message, properties=pika.BasicProperties(delivery_mode=2)
                              )
        print("Sent %r" % message)


@pytest.mark.usefixture('connect_to_rabbit', 'messages_number')
def test_consumer(connect_to_rabbit, messages_number):
    channel = connect_to_rabbit
    channel.queue_bind(exchange='test_exchange', queue="test_queue", routing_key="direct.routing.key")

    for method_frame, properties, body in channel.consume('test_queue'):
        channel.basic_ack(method_frame.delivery_tag)

        if method_frame.delivery_tag == messages_number:
            break
    requeued_messages = channel.cancel()
    print('Requeued %i messages' % requeued_messages)


