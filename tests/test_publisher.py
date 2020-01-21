import os
import pika
import sys


def test_publisher(connect_to_rabbit):
    channel = connect_to_rabbit
    channel.exchange_declare(exchange='direct_exchange', exchange_type='direct')
    channel.queue_declare(queue='test_queue', durable=True)
    channel.queue_bind(exchange='direct_exchange', queue="test_queue", routing_key="direct.routing.key")

    message = " ".join(sys.argv[1:]) or "Hello World!"

    channel.confirm_delivery()

    for i in range(10):
        channel.basic_publish(exchange='direct_exchange', routing_key='direct.routing.key',
                          body=message, properties=pika.BasicProperties(delivery_mode=2)
                          )
        print("Sent %r" % message)
    channel.close()
