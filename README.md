# Stock-Data-Streaming-ETL

Mock streaming stock data using Kafka with 2 brokers for distributed processing.

The stock data is generated randomly by stockData_generator.py. 

Stock data is generated as a list of dictionaries:
```json
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
Download Kafka through link in requirements.txt.

Extract files to main folder Stock-Data-Streaming-ETL.


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

Data Validation
---------------------------
There are two json file generated.

One called data.json under the main directory which is the original data generated before ingesting by kafka.

The other one called stock_data.json under data folder acts as data loaded into our DB.(Since we don't have a DB at the moment)

**Simulate data corruption scenario 1: Empty Value**

Open the stock_data.json file and change some values to None

**Simulate data corruption scenario 2: Missing fields**

Open the stock_data.json file and delete some fields from records

**Simulate data corruption scenario 3: Logical Error**

Such as a stock's low price is greater than it's high price. This error is generated 
by stockData_generator already. No need to change any data.

**Doing data validation**

CD into data folder,

Run the following command to do data integrity check:
```
python data_check.py
```

Summary of records passed integrity test and detail of which record failed will
appear in terminal.

The file called dataToBeReviewed.json under data folder has all the corrupted data
with error type specified for further review.

```json
[
  {
    "symbol": "MVY",
    "timestamp": 1680457995,
    "open_price": 94.44,
    "close_price": 93.37,
    "high": 95.73,
    "low": 103.31,
    "volume": 204408,
    "daily_price_change": -1.06,
    "ERROR": "LOGICAL"
  },
  {
    "symbol": "BZC",
    "timestamp": 1688068233,
    "open_price": 63.34,
    "close_price": 0,
    "high": 72.0,
    "low": 67.87,
    "volume": 307253,
    "daily_price_change": 3.0,
    "ERROR": "EMPTY VALUE"
  },
  {
    "symbol": "SLB",
    "timestamp": 1701186213,
    "open_price": 77.54,
    "close_price": 0,
    "high": 84.76,
    "low": 80.68,
    "volume": 271815,
    "daily_price_change": -8.98,
    "ERROR": "EMPTY VALUE"
  }]
```