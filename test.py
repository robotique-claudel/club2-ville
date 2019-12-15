import keras
from keras.preprocessing import image
from keras.applications import imagenet_utils
from keras.applications.mobilenet import preprocess_input
import numpy as np
from os import system
from time import sleep

mobile = keras.applications.mobilenet.MobileNet()

def prepare_image(file):
    img_path = ''
    img = image.load_img(img_path + file, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return preprocess_input(img_array_expanded_dims)

def predict(path):
    preprocessed_image = prepare_image(path)
    predictions = mobile.predict(preprocessed_image)
    results = imagenet_utils.decode_predictions(predictions)
    print(results)

while True:
    system("raspistill -o output.jpg")
    predict("output.jpg")
    sleep(2)
