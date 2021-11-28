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

from utils.messages_utils import kafka_publish_request, gpubsub_publish_request, request_router


NUM_MESSAGE_BROKER = 2 # cuurently we have 2 messaging system, kafka, 



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
    unique_id = uuid.uuid4()
    message_id = str(unique_id)

    res = request_router(unique_id, NUM_MESSAGE_BROKER)

    if res == 0:     
        kafka_publish_request(message_id, message)
    elif res == 1:
        gpubsub_publish_request(message_id, message)


def start_consuming_kafka():
    consumer = KafkaConsumer('app_messages', bootstrap_servers=KAFKA_HOST)

    for msg in consumer:
        message = json.loads(msg.value)
        if 'prediction' in message:    
            request_id = message['request_id']
            print("\033[1;32;40m ** CONSUMER: Received prediction {} for request id {}".format(message['prediction'], request_id))

def start_consuming_gpub_sub():
    """ This funciton is solely for demonstratin purpose.
    I couldn't connect to the google pub-sub system. Ideally,
    this function would consume message from google pub-sub like 
    kafka, and print the result
    """
    pass

app.router.add_get('/', index)


if __name__ == '__main__':
    threads = []
    t1 = threading.Thread(target=start_consuming_kafka)
    threads.append(t1)
    t2 = threading.Thread(target=start_consuming_gpub_sub)
    threads.append(t2)
    t1.start()
    t2.start()
    web.run_app(app, host='0.0.0.0', port=8080)
