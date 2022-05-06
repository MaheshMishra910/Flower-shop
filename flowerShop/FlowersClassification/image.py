import cv2
from keras.models import load_model
from tensorflow.python.keras.backend import get_session
import tensorflow.python.keras.backend as tb

import numpy as np
import os
import pickle
from matplotlib import pyplot as plt
from keras.models import load_model

import joblib


def predict_one_image(img, model):
    img = cv2.resize(img, (128, 128), interpolation = cv2.INTER_CUBIC)
    img = np.reshape(img, (1, 128, 128, 3))
    img = img/255.
    pred = model.predict(img)
    class_num = np.argmax(pred)
    return class_num, np.max(pred)


def process_image(uploaded_file):
    # tb._SYMBOLIC_SCOPE.value = True
    model = load_model('model/classification4.h5')

    
    flower =  ['daisy', 'sunflower', 'rose', 'dandelion', 'tulip']
    # flower = ["daisy","dandelion", "rose","sunflower","tulip"]
    test_img = plt.imread('media/'+ uploaded_file)
    pred, probability = predict_one_image(test_img, model)
    if probability > 0.4:
        text = "This is   " + flower[pred]
    else:
        text = "This is not a flower. Please upload flower photos"
        
    return flower[pred], round(probability, 2)*100 , text
    



