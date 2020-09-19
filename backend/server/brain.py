import base64
import numpy as np
import io
from PIL import Image
import warnings
warnings.filterwarnings("ignore")
import keras
from keras import backend as K
from keras.models import Sequential, load_model
from keras.preprocessing.image import ImageDataGenerator, img_to_array
from flask import Flask, render_template, jsonify, request
from io import BytesIO
from keras import layers

app = Flask(__name__)

def get_model():
    encoder_input = keras.Input(shape=(224, 224, 3), name="img")
    x = layers.Conv2D(16, 3, activation="relu")(encoder_input)
    x = layers.Conv2D(32, 3, activation="relu")(x)
    x = layers.MaxPooling2D(3)(x)
    encoder_output = layers.Conv2D(32, 3, activation="relu")(x)

    encoder = keras.Model(encoder_input, encoder_output, name="encoder")
    print("Model loaded!")
    return encoder

def preprocess_image(image,target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis = 0)

    return image

num = 4
@app.route("/")
@app.route("/index")
def index():
    my_list = []
    for j in range(num):
        my_list.append(j)
    return render_template('index.html', max_num = num, arr = my_list)

@app.route("/predict", methods = ["POST"])
def predict():
    message = request.get_json(force = True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size = (224, 224))

    model = get_model()
    prediction = []
    for i in range(num):
        prediction.append(model.predict(processed_image)[0, ..., i])

    response = {}

    for i in range(num):
        res = Image.fromarray(((prediction[i] + 1) / 2 * 255).astype("uint8"))
        buff = BytesIO()
        res.save(buff, format="PNG") 
        result = base64.b64encode(buff.getvalue()).decode("utf-8")

        response["image" + str(i)] = result

        print(result)
    
    # response = {
    #     'image': result
    # }
    return jsonify(response)
