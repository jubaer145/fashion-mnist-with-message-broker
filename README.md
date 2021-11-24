### Part-1
Use ```vector_ai_fashion_mnist.ipynb``` to train multi-class classification model. For inferencing, currently I am taking the index of the test dataframe, and giving the prediciton. This can be processed in any way.

### Part-2 and Part-3
I haven't yet created a unified api, but working on it. Currently I'm only using ```kakfa``` as my message broker.

Run ```app.py``` in one terminal. It'll create an ```aiohttp``` server, on top of ```socketio``` server. Client can communicate with it using socket. Then, this server communicates with ```Kafka```, publishing it's client request.  I have created a sample ```index.html```, where you give index of the test dataset of fashion-mnish, it'll print the output on the command-line.

Run ```predictor.py``` in another terminal, it'll consume the published message from the server, and load the sample of the given index from the test dataset. It'll then predict and publish it's prediction to ```kafka```. 