import pika
import pytest


@pytest.mark.usefixture('connect_to_rabbit', 'config_parser')
def test_publisher(connect_to_rabbit, config_parser):
    channel = connect_to_rabbit
    message = "Hello World!"
    channel.confirm_delivery()
    for i in range(int(config_parser["messages"])):
        channel.basic_publish(exchange='test_exchange', routing_key='direct.routing.key',
                              body=message, properties=pika.BasicProperties(delivery_mode=2)
                              )
        print("Sent %r" % message)


@pytest.mark.usefixture('connect_to_rabbit', 'config_parser')
def test_consumer(connect_to_rabbit, config_parser):
    channel = connect_to_rabbit
    channel.queue_bind(exchange='test_exchange', queue="test_queue", routing_key="direct.routing.key")

    for method_frame, properties, body in channel.consume('test_queue'):
        channel.basic_ack(method_frame.delivery_tag)

        if method_frame.delivery_tag == int(config_parser["messages"]):
            break
    requeued_messages = channel.cancel()
    print('Requeued %i messages' % requeued_messages)


