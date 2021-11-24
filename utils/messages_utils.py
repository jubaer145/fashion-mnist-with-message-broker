import json

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

def publish_prediction(pred, request_id):
	print('**********printing prediction***************')
	producer.send('app_messages', json.dumps({'request_id': request_id, 'prediction': pred}).encode('utf-8'))
	producer.flush()