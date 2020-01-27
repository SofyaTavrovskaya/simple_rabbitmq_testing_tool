import pika
import sys
import pytest


#@pytest.mark.usefixture('connect_to_rabbit', 'messages_number')
def test_publisher(connect_to_rabbit, messages_number=10):
    channel = connect_to_rabbit
    channel.exchange_declare(exchange='direct_exchange', exchange_type='topic')
    channel.queue_declare(queue='test_queue', durable=True)
    channel.queue_bind(exchange='direct_exchange', queue="test_queue", routing_key="direct.routing.key")

    message = " ".join(sys.argv[1:]) or "Hello World!"

    channel.confirm_delivery()
    for i in range(messages_number):
        channel.basic_publish(exchange='direct_exchange', routing_key='direct.routing.key',
                              body=message, properties=pika.BasicProperties(delivery_mode=2)
                              )
        print("Sent %r" % message)
    channel.close()


def test_consumer(connect_to_rabbit, messages_number=10):
    channel = connect_to_rabbit
    channel.queue_bind(exchange='direct_exchange', queue="test_queue", routing_key="direct.routing.key")

    for method_frame, properties, body in channel.consume('test_queue'):
        print(method_frame)
        print(properties)
        print(body)

        channel.basic_ack(method_frame.delivery_tag)

        if method_frame.delivery_tag == messages_number:
            break
    requeued_messages = channel.cancel()
    print('Requeued %i messages' % requeued_messages)

    # Close the channel and the connection
    channel.close()

