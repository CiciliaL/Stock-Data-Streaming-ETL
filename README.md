# Stock-Data-Streaming-ETL

Mock streaming stock data using Kafka with 2 brokers for distributed processing.

The stock data is generated randomly by stockData_generator.py. 

Stock data is generated as a list of dictionaries:
```
[
  {
    "symbol": "NXB",
    "timestamp": 1675716880,
    "open_price": 80.95,
    "close_price": 82.97,
    "high": 86.08,
    "low": 71.42,
    "volume": 186521,
    "daily_price_change": 2.02
  }
  ]
```
Data transformation such as calculating daily_price_change is done before ingesting data for maximum efficiency of streaming.

Usage
-------------------

Open a terminal to clone repo and cd into directory.

```
git clone https://github.com/CiciliaL/Stock-Data-Streaming-ETL.git
cd Stock-Data-Streaming-ETL
```


Starting Kafka Servers
----------------------

**cd into Kafka folder and Start Zookeeper**
```
cd kafka_2.13-3.6.1
bin/zookeeper-server-start.sh config/zookeeper.properties
```
**Create 2 config files for 2 brokers**
```
cp config/server.properties config/server.1.properties
cp config/server.properties config/server.2.properties
```
To create 2 brokers, we also need to change the properties file so that they are unique
open these two new properties file and look for the following properties
**server.1.properties**
```
broker.id=1
listeners=PLAINTEXT://:9093
log.dirs=/tmp/kafka-logs1
```
**server.2.properties**
```
broker.id=2
listeners=PLAINTEXT://:9094
log.dirs=/tmp/kafka-logs2
```
**Create log directories**
```
mkdir /tmp/kafka-logs1
mkdir /tmp/kafka-logs2
```
**Start 2 broker instances**

Run the first command:
```
bin/kafka-server-start.sh config/server.1.properties
```
Open a new terminal session and run the second command:
```
bin/kafka-server-start.sh config/server.2.properties
```
Once started successfully, the following message should appear:
```
[2023-12-08 20:08:43,025] INFO Kafka version: 3.6.1 (org.apache.kafka.common.utils.AppInfoParser)

[2023-12-08 20:08:43,026] INFO Kafka commitId: 5e3c2b738d253ff5 (org.apache.kafka.common.utils.AppInfoParser)

[2023-12-08 20:08:43,026] INFO Kafka startTimeMs: 1702084123018 (org.apache.kafka.common.utils.AppInfoParser)

[2023-12-08 20:08:43,028] INFO [KafkaServer id=1] started (kafka.server.KafkaServer)
```

Creating Topics
------------------
**Create a topic**
default topic name is 'stock_data', if you need to change the topic, remember to also change the topic variable in kafka_config.py
```
bin/kafka-topics.sh --create --topic stock-data --bootstrap-server localhost:9093 --partitions 2 --replication-factor 2
```
Once you created the topic successfully, you should see a message:
```
Created topic stock-data.
```

Starting Consumer
---------------------
cd into Stock-Data-Streaming-ETL folder 

type in commands to start our consumer:
```
python kafka_consumer.py stock-data
```

Starting Producer
------------------
commands to start our producer:
```
python kafka_producer.py stock-data
```