from confluent_kafka import Producer
import json
from data import stockData_generator
import logging
import kafka_config
import time


def error_report(err, msg):
    """
    Logs the status of message delivery.

    This function is used as callback for reporting the status of message delivery in our Kafka producer
    If an error occurred during delivery, an error message is logged. Otherwise, an informational message
    indicating the successful delivery, including details such as the topic, partition, and offset, is logged.

    :param err: An error object representing the reason for message delivery failure.
    :param msg: The Kafka message that was delivered or failed to deliver.
    :return: None
    """
    if err is not None:
        logging.error(f'Message delivery failed: {err}')
    else:
        logging.info(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')


def produce_messages(server, topic, stock_data):
    """
    KAfka producer that produces to given topic

    :param server: The Kafka server configuration, configurable in kafka_config.py.
    :param topic: The Kafka topic to which messages will be produced, configurable in kafka_config.py.
    :param stock_data: A list of messages (stock data, data format is list of dictionaries) to be produced to the Kafka topic.
    :return: None
    """
    conf = {
        'bootstrap.servers': server,
        'acks': 1,
        'retries': 5,
        'retry.backoff.ms': 100
    }  # producer requires at least one acknowledgement to consider message sent to prevent data loss
    producer = Producer(conf)

    try:
        for data in stock_data:
            producer.produce(topic, json.dumps(data), callback=error_report)

        producer.flush()

    except Exception as e:
        logging.error(f'Exception Raised in produce_message:{e}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bootstrap_servers = kafka_config.bootstrap_servers  # modify in kafka_config
    topic = kafka_config.topic  # modify in kafka_config

    n = 0
    while n < 30:
        try:
            stock_data = stockData_generator.generate_mock_stock_data(num_records=10)
            produce_messages(bootstrap_servers, topic, stock_data)
            stockData_generator.generate_json_file('data.json', stock_data)
            n += 1
            time.sleep(0.5)

        except KeyboardInterrupt:
            logging.info('Received KeyboradInterrupt. Kafka producer stopped.')
            break

        except json.JSONDecodeError as e:
            logging.error(f'Error decoding JSON: {e}')

        except Exception as e:
            logging.error(f'Exception raised. Error code:{e}')


