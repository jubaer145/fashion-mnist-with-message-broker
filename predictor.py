import torch
import json
import os
import numpy as np
import pandas as pd
from model.model import get_model
from utils.preprocessor_utils import get_preprocessor
from utils.messages_utils import kafka_publish_prediction, request_router, gpubsub_publish_prediction

from kafka import KafkaConsumer

torch.manual_seed(13)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')



test_df = pd.read_csv("/media/jubaer/DataBank/karma/fashion_mnist_ds/archive/fashion-mnist_test.csv")


KAFKA_HOST = 'localhost:9092'
TOPICS = 'app_messages'
consumer = None
model = None

def get_label(idx):
    idx2cat_mapping = {
                 0: "T-shirt/Top",
                 1: "Trouser",
                 2: "Pullover",
                 3: "Dress",
                 4: "Coat", 
                 5: "Sandal", 
                 6: "Shirt",
                 7: "Sneaker",
                 8: "Bag",
                 9: "Ankle Boot"
                 }
    index = (idx.item() if type(idx) == torch.Tensor else idx)
    return idx2cat_mapping[index]


def load_model(checkpoint_path):
    model = get_model()

    if device == torch.device('cpu'):
        checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        checkpoint = torch.load(checkpoint_path)
        model.load_state_dict(checkpoint['model_state_dict'])
    return model



def df2image(idx):
    """ It takes the index of the test df of the fashion_mnist
        dataset, converts the 1-D array to a 2-D image, and returns
        it.     
    """
    sample = test_df.iloc[idx]
    # true_label = sample[0]  ## 1st entry is the label, for sanity checking
    image = sample[1:]
    image = np.asarray(image).reshape(28, 28, 1).astype('float32') / 255.0
    transformer = get_preprocessor()
    image = transformer(image).unsqueeze(0)
    return image

def predict(img):
    idx = torch.argmax(torch.exp(model(img)))
    return get_label(idx)
    


def start():
    print('***************Started*****************')
    for msg in consumer:
        message = json.loads(msg.value)
        if 'data' in message:
            request_id = message['request_id']
            broker = message['broker']
            print(message)
            img_id = message['data']  ## this image id represents the original image path. In our case, it the index of the test dataframe of the fashionmnist
            img = df2image(img_id)
            label = predict(img)
            if broker == 0:
                kafka_publish_prediction(request_id, label)
            elif broker == 1:
                gpubsub_publish_prediction(request_id, label)  ## this is only for demo purpuse


if __name__ == '__main__':
    checkpoint_version = "v1.pth"
    checkpoint_path = os.path.join(*[os.getcwd(), "model", "weights", checkpoint_version])
    model = load_model(checkpoint_path)
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_HOST)
    consumer.subscribe(TOPICS)
    start()




