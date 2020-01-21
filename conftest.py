import pika
import pytest
import os
import configparser


@pytest.fixture()
def connect_to_rabbit():
    user_name = os.environ.get('RABBIT_USER')
    password = os.environ.get('RABBIT_PASSWORD')
    credentials = pika.PlainCredentials(user_name, password)
    parameters = pika.ConnectionParameters('172.17.0.2',
                                           5672,
                                           '/',
                                           credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    return channel


@pytest.fixture()
def messages_number():
    config = configparser.ConfigParser()
    config.read('./fixtures/config.ini')
    number_of_messages = config['messages']['number_of_massages']
    return number_of_messages


