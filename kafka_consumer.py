from confluent_kafka import Consumer
import json
import logging
import kafka_config


def write_message_to_json(msg, output_file):
    """
    Write message to a JSON file. Using this as substitute for DB.

    :param msg: The message data to be written to the JSON file.
    :param output_file: The path to the JSON file.
    :return: None
    """
    with open(output_file, 'a') as json_file:
        json.dump(msg, json_file)
        json_file.write('\n')


def consume_messages(server, topic, output_file, timeout_sec=10.0):
    """
    Consume messages from given topics and write them to DB.
    Since there is no available DB currently, we will write to a json file
    for downstream analytics and data integrity check.

    :param server: The Kafka server configuration, configurable in kafka_config.py.
    :param topic: The Kafka topic to which our consumer subscribed, configurable in kafka_config.py.
    :return: None
    """
    conf = {
        'bootstrap.servers': server,
        'group.id': 'my_group',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)
    consumer.subscribe([topic])

    message_count = 0
    try:
        while True:
            msg = consumer.poll(timeout_sec)

            if msg is None:
                logging.info(f'No New data received for {timeout_sec} seconds')
                logging.info(f'Total messages received: {message_count}')
                break
            if msg.error():
                logging.error(f'Error: {msg.error()}')
            else:
                message_data = json.loads(msg.value().decode("utf-8"))
                write_message_to_json(message_data, output_file)
                logging.info(f'Received and written to JSON: {message_data}')
                message_count += 1  # to keep track of num of messages polled

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bootstrap_servers = kafka_config.bootstrap_servers
    topic = kafka_config.topic

    consume_messages(bootstrap_servers, topic, './stock_data.json', timeout_sec=12.0)
