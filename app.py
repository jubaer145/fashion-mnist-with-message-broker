from aiohttp import web
import socketio
import pandas as pd
import json
import asyncio
import threading
from queue import Queue
import uuid

from pathlib import Path
from kafka import KafkaProducer, KafkaConsumer
from time import sleep


sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


PATH = Path('data/')
KAFKA_HOST = 'localhost:9092'

async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('message')
def start_producing(sid, message):
	print(message)
	producer = KafkaProducer(bootstrap_servers=KAFKA_HOST)
	message_id = str(uuid.uuid4())
	message = {'request_id': message_id, 'data': json.loads(message)}

	producer.send('app_messages', json.dumps(message).encode('utf-8'))
	producer.flush()

	print("\033[1;31;40m -- PRODUCER: Sent message with id {}".format(message_id))




def start_consuming():
    consumer = KafkaConsumer('app_messages', bootstrap_servers=KAFKA_HOST)

    for msg in consumer:
        message = json.loads(msg.value)
        if 'prediction' in message:    
            request_id = message['request_id']
            print("\033[1;32;40m ** CONSUMER: Received prediction {} for request id {}".format(message['prediction'], request_id))


app.router.add_get('/', index)


if __name__ == '__main__':
    threads = []
    t = threading.Thread(target=start_consuming)
    threads.append(t)
    t.start()
    web.run_app(app, host='0.0.0.0', port=8080)
