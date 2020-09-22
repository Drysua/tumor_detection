import base64
import numpy as np
import io
from PIL import Image
import warnings
import json
warnings.filterwarnings("ignore")
import keras
from keras import backend as K
from keras.models import Sequential, load_model
from keras.preprocessing.image import ImageDataGenerator, img_to_array
from flask import Flask, render_template, jsonify, request, redirect, Response
from io import BytesIO
from keras import layers
from flask_cors import CORS
from neural.classifier_process import *
import os
import jsonpickle

cwd = os.getcwd()

app = Flask(__name__)
CORS(app)

model_path = "./backend/server/neural/model.h5"
model = load_model(model_path, compile = False)
print(" * Model loaded!")


def preprocess_image(image,target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis = 0)

    return image

# print("* Loading Keras model...")
# get_model()

# num = 4
# @app.route("/")
# @app.route("/index")
# def index():
#     return render_template('predict.html')


@app.route("/form", methods = ["POST"])
def predict():
    message = request.get_json(force = True)
    print(message)
    encoded = message['image']
    img_name = message['name']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size = (224, 224))
    imgs = processed_image.reshape([1, 224, 224, 3])

    prediction = classifier_process(model, imgs, threshold = 0.5)
    print(prediction)


    response = {
        "Labels": prediction[0],
        "id": img_name
    }


    return jsonify(response)

@app.route("/predict", methods = ["POST"])
def upload_file():
    print(request.files)
    if(request.method == 'POST'):
        img = request.files['file']
        img_name = img.filename
        decoded = img.read()
        image = Image.open(io.BytesIO(decoded))
        processed_image = preprocess_image(image, target_size = (224, 224))
        imgs = processed_image.reshape([1, 224, 224, 3])

        prediction = classifier_process(model, imgs, threshold = 0.5)
        print(prediction)


        response = {
            "Labels": prediction[0],
            "id": img_name
        }

        response_pickled = jsonpickle.encode(response)

        return Response(response=response_pickled, status=200, mimetype="application/json")
        # return response_pickled

@app.route("/joke", methods = ["POST"])
def joke():
    print(request.files['file'])
    return "ok"
    

