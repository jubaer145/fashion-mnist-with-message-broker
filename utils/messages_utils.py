import json
import hashlib

from kafka import KafkaProducer

kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092')
gpub_sub_producer = "Demo Producer"  ## This is for demo purpose. I couldn't connect to google pub-sub

def kafka_publish_prediction(request_id, pred):
	print('**********Kafka Publising***************')
	kafka_producer.send('app_messages', json.dumps({'request_id': request_id, 'prediction': pred, 'broker': 0}).encode('utf-8'))
	kafka_producer.flush()
	print(f"\033[1;31;40m -- PRODUCER-KAFKA: Sent prediction message with id {message_id}")

def gpubsub_publish_prediction(request_id, pred):
	print('**********Kafka Publising***************')
	kafka_producer.send('app_messages', json.dumps({'request_id': request_id, 'prediction': pred, 'broker': 1}).encode('utf-8'))
	kafka_producer.flush()
	print(f"\033[1;31;40m -- PRODUCER-KAFKA: Sent prediction message with id {message_id}")



def kafka_publish_request(message_id, message):
	message = {'request_id': message_id, 'data': json.loads(message), 'broker': 0}
	kafka_producer.send('app_messages', json.dumps(message).encode('utf-8'))
	kafka_producer.flush()
	print(f"\033[1;31;40m -- PRODUCER-KAFKA: Sent request message with id {message_id}")


def gpubsub_publish_request(message_id, message):
	message = {'request_id': message_id, 'data': json.loads(message), 'broker': 1}
	print(f"{gpub_sub_producer}")  ## demo calling the google pub-sub producer
	print(f"\033[1;31;40m -- PRODUCER: Sent request message with id {message_id}")


def request_router(unique_id, num_message_broker):
	""" This function receives a request id, generates a 
	hash, and distribute the request according to the 
	moduls of total number of broker
	"""
	x = hashlib.sha256(unique_id.bytes).hexdigest() 
	num_broker = int(x, 16) % num_message_broker
	return num_broker




