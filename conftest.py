import pika
import pytest
import configparser


@pytest.fixture(scope="session")
def connect_to_rabbit(config_parser):
    user_name = config_parser["user_name"]
    password = config_parser["password"]
    credentials = pika.PlainCredentials(user_name, password)
    parameters = pika.ConnectionParameters(host=config_parser["host"], port=int(config_parser["port"]),
                                           virtual_host=config_parser["virtual_host"], credentials=credentials)
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
def config_parser():
    config = configparser.ConfigParser()
    config.read('./fixtures/config.ini')
    config_dict = {'user_name': config['credentials']['username'],
                   'password': config['credentials']['password'],
                   'messages': config['messages']['number_of_messages'],
                   'host': config['credentials']['host'],
                   'port': config['credentials']['port'],
                   'virtual_host': config['credentials']['virtual_host']
                   }
    yield config_dict

