Minimal tests for containerized RabbitMQ using pytest and Pika

How to run:
1. Install requirements to python venv or globally
2. Run docker container with RabbitMQ:
   $ docker run -d --hostname my-rabbit --name some-rabbit -p 8080:15672 rabbitmq:3-management
   You can then go to http://localhost:8080 or http://host-ip:8080 in a browser with the default username and password
    of guest / guest
3. The tests test_publisher and test_consumer are wrapped in pytest. To run pytest you should specify in fixtures
/config.ini necessary parameters. For example, host name, port, number of messages etc.
 python producer.py - it
4. Run test:
   $ pytest - it should run without errors


