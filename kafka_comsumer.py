from confluent_kafka import Consumer
import json
import logging
import kafka_config


def write_message_to_json(msg, output_file):
    """
    Write message to a JSON file.

    :param msg: The message data to be written to the JSON file.
    :param output_file: The path to the JSON file.
    :return: None
    """
    with open(output_file, 'a') as json_file:
        json.dump(msg, json_file)
        json_file.write('\n')


def consume_messages(server, topic, output_file):
    """
    Consume messages from given topics and write them to DB.
    Since there is no available DB currently, we will write to a json file
    for downstream analytics and data integrity check.

    :param server: The Kafka server configuration, configurable in kafka_config.py.
    :param topic: The Kafka topic to which our consumer subscribed, configurable in kafka_config.py.
    :return: None
    """
    conf = {'bootstrap.servers': server, 'group.id': 'my_group', 'auto.offset.reset': 'earliest'}
    consumer = Consumer(conf)
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                logging.error(f'Error: {msg.error()}')
            else:
                message_data = json.loads(msg.value().decode("utf-8"))
                write_message_to_json(message_data, output_file)
                logging.info(f'Received and written to JSON: {message_data}')
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == '__main__':
    bootstrap_servers = kafka_config.bootstrap_servers
    topic = kafka_config.topic

    consume_messages(bootstrap_servers, topic, './stock_data.json')
