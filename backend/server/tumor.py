import base64
import numpy as np
import io
from PIL import Image
import warnings
import json
warnings.filterwarnings("ignore")
# import keras
# from keras import backend as K
# from keras.models import Sequential, load_model
# from keras.preprocessing.image import ImageDataGenerator, img_to_array
from flask import Flask, render_template, jsonify, request
from io import BytesIO
# from keras import layers
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model_name = "hello.h5"

# def get_model():
#     global model
#     model = load_model(model_name)
#     print(" * Model loaded!")

# def preprocess_image(image,target_size):
#     if image.mode != "RGB":
#         image = image.convert("RGB")
#     image = image.resize(target_size)
#     image = img_to_array(image)
#     image = np.expand_dims(image, axis = 0)

#     return image

# print("* Loading Keras model...")
# get_model()

# num = 4
# @app.route("/")
# @app.route("/index")
# def index():
#     return render_template('predict.html')


@app.route("/predict", methods = ["POST"])
def predict():
    message = request.get_json(force = True)
    # encoded = message['image']
    # decoded = base64.b64decode(encoded)
    # image = Image.open(io.BytesIO(decoded))
    # processed_image = preprocess_image(image, target_size = (224, 224))

    # prediction = model.predict(processed_image)
    prediction = np.random.random(14)


    response = {
        #'prediction' : json.dumps({
        'atelectasis': prediction[0],
        'cardiomegaly': prediction[1],
        'effusion': prediction[2],
        'infiltration': prediction[3],
        'mass': prediction[4],
        'nodule': prediction[5],
        'pneumonia': prediction[6],
        'pneumothorax': prediction[7],
        'consolidation': prediction[8],
        'edema': prediction[9], 
        'emphysema': prediction[10],
        'fibrosis': prediction[11],
        'pleural_thickening': prediction[12],
        'hernia': prediction[13]
        
    }


    return jsonify(response)
