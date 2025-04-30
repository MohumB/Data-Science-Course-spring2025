from confluent_kafka import Producer, Consumer, TopicPartition
import json
import logging
from datetime import datetime, timedelta
import time


logging.basicConfig(level = logging.INFO, format = "%(asctime)s %(levelname)s %(message)s")

conf = {
    'bootstrap.servers': 'kafka:9092', 
    'group.id': 'transaction_consumer-group',
    'auto.offset.reset': 'earliest',
    # 'api.version.request': False, # depricated
    'socket.timeout.ms': 1600, # Increased to ensure it's at least 1000ms higher than fetch.wait.max.ms
    'security.protocol': 'PLAINTEXT',
}

consumer = Consumer(conf)
consumer.subscribe(['darooghe.transactions'])


    
err_producer = Producer({'bootstrap.servers': 'kafka:9092'})

for _ in range(10):  # Wait up to 50 seconds
    topics = consumer.list_topics().topics
    if 'darooghe.transactions' in topics:
        break
    logging.info("Waiting for topic...")
    time.sleep(5)
    
    
def delivery_report(err, msg):
    if err:
        logging.error(f"Message delivery failed: {err}")
    else:   
        logging.debug(f"Error logged to {msg.topic()} [Partition: {msg.partition()}]")
        
def validate_amount(transaction):
    total_amount_expected = transaction['amount'] + transaction['vat_amount']
    + transaction['commission_amount']
    
    return total_amount_expected, transaction['total_amount'] == total_amount_expected


def validate_time(transaction, errors):
    try:
        transaction_time = datetime.fromisoformat(transaction['timestamp'].replace('Z',
            ''))
    
        current_time = datetime.utcnow()
        time_diff = current_time - transaction_time

        if transaction_time > current_time:
            errors.append({
                "code" : "ERR_TIME",
                "message" : f'Transaction time is in the future. Transaction time: {transaction_time}, Current time: {current_time}'
            })

        elif time_diff > timedelta(days = 1):
            errors.append({
                "code" : "ERR_TIME",
                "message" : f'Transaction time is older than 24 hours. Transaction time: {transaction_time}, Current time: {current_time}'
            })
    except Exception as e:
        errors.append({
            "code" : "ERR_TIME",
            "message" : f'Invalid timestamp format: {e}'
        })
    
def validate_device(transaction):
    if transaction['payment_method'] == 'mobile':
        if 'device_info' not in transaction or transaction['device_info'].get('os') not in ['iOS', 'Android']:
            return False
    return True


def validate_transaction(transaction):
    errors = []
    
    total_amount_expected, is_amount_validated = validate_amount(transaction)
    
    if not is_amount_validated:
        errors.append({
            "code" : "ERR_AMOUNT",
            "message" : f'Total amount mismatch. Expected {total_amount_expected}, got {transaction["total_amount"]}'
        }
        )
        
    validate_time(transaction, errors)    
    
    is_device_valid = validate_device(transaction)
    if not is_device_valid:
        errors.append({
            "code" : "ERR_DEVICE",
            "message" : f'Invalid device information for payment method {transaction["payment_method"]}'
        })
    return errors

   
def process_transaction(msg):
    try:
        transaction = json.loads(msg.value())
        logging.debug(f"Processing transaction: {transaction['transaction_id']}")
        
       
        errors = validate_transaction(transaction)
        
        if errors:
            
            error_message = {
                "transaction_id": transaction['transaction_id'],
                "errors": errors,
                "original_data": transaction
            }
            err_producer.produce(
                'darooghe.error_logs',
                key=transaction['transaction_id'],
                value=json.dumps(error_message),
                callback=delivery_report
            )
            err_producer.flush()
            #logging.warning(f"Invalid transaction detected: {transaction['transaction_id']}")
        else:
            logging.debug(f"Valid transaction: {transaction['transaction_id']}")
    
    except json.JSONDecodeError:
        logging.error("Failed to decode message")
    except KeyError as e:
        logging.error(f"Missing field in transaction: {e}")


try:
    while True:
        msg = consumer.poll(1.0)  
        if msg is None:
            continue
        if msg.error():
            logging.error(f"Consumer error: {msg.error()}")
        else:
            process_transaction(msg)
except KeyboardInterrupt:
    logging.info("Shutting down consumer...")
finally:
    consumer.close()   
        