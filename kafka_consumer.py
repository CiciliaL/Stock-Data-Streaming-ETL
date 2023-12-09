from confluent_kafka import Consumer
import json
import logging
import kafka_config
import time


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


def consume_messages(server, topic, output_file, timeout_sec=15):
    """
    Consume messages from given topics and write them to DB.
    Since there is no available DB currently, we will write to a json file
    for downstream analytics and data integrity check.

    :param server: The Kafka server configuration, configurable in kafka_config.py.
    :param topic: The Kafka topic to which our consumer subscribed, configurable in kafka_config.py.
    :param timeout_sec: Time interval if consumer did not receive new message for, consumer will shut down.
    :return: None
    """
    conf = {'bootstrap.servers': server, 'group.id': 'my_group', 'auto.offset.reset': 'earliest'}
    consumer = Consumer(conf)
    consumer.subscribe([topic])

    start_time = time.time()

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                elapsed_time = time.time() - start_time
                if elapsed_time >= timeout_sec:
                    logging.info(f'No New data received for {timeout_sec} seconds')
                    break
                continue
            if msg.error():
                logging.error(f'Error: {msg.error()}')
            else:
                message_data = json.loads(msg.value().decode("utf-8"))
                write_message_to_json(message_data, output_file)
                logging.info(f'Received and written to JSON: {message_data}')

                start_time = time.time()  # reset the time if new message received
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bootstrap_servers = kafka_config.bootstrap_servers
    topic = kafka_config.topic

    consume_messages(bootstrap_servers, topic, './stock_data.json')
