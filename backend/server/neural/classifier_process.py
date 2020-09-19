import keras
import keras.backend as K
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Activation, Flatten, Dropout, BatchNormalization, Conv2D, MaxPooling2D
from keras import regularizers, optimizers
from keras import Input, Model
from keras.applications import MobileNet, ResNet50

import numpy as np
import pandas as pd 

def classifier_process(model, imgs, threshold = 0.5):
  classes = ["Atelectasis", "Cardiomegaly", "Effusion",\
             "Infiltration", "Mass", "Nodule", "Pneumonia",\
             "Pneumothorax", "Consolidation", "Edema",\
             "Emphysema", "Fibrosis", "Pleural_Thickening", "Hernia"]
  
  pred = model.predict(imgs)
  print(pred)
  predict_list = []
  img_num = pred[0].shape[0]
  
  for i in range(img_num):
    img_list = []
    for j, cl in enumerate(classes):
      if pred[j][i] > threshold:
        img_list.append(cl)
    predict_list.append(img_list)
  return predict_list