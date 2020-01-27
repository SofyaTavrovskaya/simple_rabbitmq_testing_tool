import pika
import pytest
import os
import configparser


@pytest.fixture(scope="session")
def connect_to_rabbit():
    user_name = os.environ.get('RABBIT_USER')
    password = os.environ.get('RABBIT_PASSWORD')
    credentials = pika.PlainCredentials(user_name, password)
    parameters = pika.ConnectionParameters('172.17.0.2', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange='test_exchange', exchange_type='topic')
    channel.queue_declare(queue='test_queue', durable=True)
    channel.queue_bind(exchange='test_exchange', queue="test_queue", routing_key="direct.routing.key")
    yield channel
    channel.queue_unbind(queue='test_queue', exchange='test_exchange', routing_key='direct.routing.key')
    channel.queue_delete(queue='test_queue', if_unused=False, if_empty=False)
    channel.exchange_delete(exchange='direct_exchange', if_unused=False)
    channel.close()
    connection.close()


@pytest.fixture(scope="session")
def messages_number():
    config = configparser.ConfigParser()
    config.read('./fixtures/config.ini')
    number_of_messages = int(config['messages']['number_of_messages'])
    yield number_of_messages

