# Real-Time E-commerce Order Processing Pipeline using Amazon SNS, SQS, and Cassandra

## Overview

This project demonstrates a real-time, scalable data processing pipeline for an e-commerce platform. It uses **Amazon SNS** and **Amazon SQS** to implement a fan-out messaging architecture. Producers publish `order` data to an SNS topic, which distributes the messages to multiple SQS queues for independent processing by consumers. The processed data is stored in a **local Cassandra database**, making it ready for further analytics or reporting.

---

## Project Workflow

1. **Data Generation (Producer)**:
   - The `order_producer.py` script generates mock order data (e.g., `order_id`, `customer_id`, `item`, etc.) and publishes it to an **SNS topic (`orders_topic`)**.

2. **Message Fan-Out (SNS)**:
   - The SNS topic (`orders_topic`) forwards messages to two SQS queues:
     - **Order Processing Queue** (`order_processing_queue`): For inserting order data into Cassandra.
     - **Analytics Queue** (`analytics_queue`): For logging data for analytics.

3. **Data Consumption (Consumers)**:
   - **Order Consumer**:
     - Reads messages from the `order_processing_queue`.
     - Inserts the order data into the Cassandra database.
   - **Analytics Consumer**:
     - Reads messages from the `analytics_queue`.
     - Logs the order data for analytics.

4. **Database Storage**:
   - A **denormalized Cassandra table** stores processed order data for easy querying and downstream analysis.

---

## Architecture Diagram

```plaintext
  +------------------------------------------+
  |             Order Producer               |
  +------------------------------------------+
                        |
                        |
                        v
  +------------------------------------------+
  |               SNS Topic                  |
  +------------------------------------------+
          |                       |
          | Publish Orders         | Fan-Out to Subscribers
          v                       v
  +-------+-------+       +-------+----------+
  | SQS Order Proc|       |   SQS Analytics  |
  +---------------+       +------------------+
          |                       |
          | Consume Orders         | Consume Orders
          v                       v
  +---------------+       +------------------+
  | Order Consumer|       | Analytics Consumer|
  +-------+-------+       +-------+----------+
          |                       |
          | Insert into Cassandra | Log Analytics
          v                       v
  +-------------------------------------------+
  |     Local Cassandra (orders_payments_facts)|
  +-------------------------------------------+
```


## Setup Instructions

Step 1: **Set Up Cassandra**

1. Install Docker and start Cassandra using the provided docker-compose.yml
```bash
cd cassandra
docker-compose up -d
```

2. Set up the database schema by running schema.cql in cqlsh:
```bash
docker exec -it cassandra-db cqlsh
SOURCE 'schema.cql';
```


Step 2: **Set Up Amazon SNS and SQS**
1. Log in to your AWS Management Console.
2. Create an SNS Topic:
    - Name: orders_topic.
3. Create Two SQS Queues:
    - order_processing_queue
    - analytics_queue
4. Subscribe the SQS Queues to the SNS Topic:
5. In the SNS Topic's "Subscriptions" section, add:
    - A subscription to order_processing_queue.
    - A subscription to analytics_queue.
Note down the SNS Topic ARN and SQS Queue URLs for use in the scripts.


Step 3: **Install Dependencies**
```bash
cd producer
pip install -r requirements.txt
```

Step 4: **Run the Producer**
```bash
python producer/order_producer.py
```

Step 5: **Run the Consumers**
1. Order Consumer:
```bash
python consumer/order_consumer.py
```

2. Analytics Consumer:
```bash
python consumer/analytics_consumer.py
```

Step 6: **Verify Data**
```bash
SELECT * FROM ecom_store.orders_payments_facts;
```