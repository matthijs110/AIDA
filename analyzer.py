import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import tensorflow as tf
import pathlib
import shutil
import os
from tensorflow import keras


def analyze(config, pbTotal):

    physical_devices = tf.config.list_physical_devices('GPU') 
    for gpu_instance in physical_devices: 
        tf.config.experimental.set_memory_growth(gpu_instance, True)

    img_height = config['image']['resolution']
    img_width = config['image']['resolution']
    source_path = pathlib.Path(f"{config['tmpdirectory']}/images/all")
    img_dest_path = pathlib.Path(f"{config['tmpdirectory']}/images/filtered/")

    np.set_printoptions(suppress=True)
    # only use model2 or model4

    model = tensorflow.keras.models.load_model('model4')

    images = list(source_path.glob('*.jpeg'))

    for image in images:

        if(os.stat(image).st_size > 5000):

            img = keras.preprocessing.image.load_img(
                image, target_size=(img_height, img_width)
            )
            img_array = keras.preprocessing.image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)  # Create a batch

            # run the inference
            prediction = model.predict(img_array)
            score = tf.nn.softmax(prediction[0])

            class_names = ['set1', 'set2']

            if class_names[np.argmax(score)] == 'set1':
                shutil.copy(image, img_dest_path)

        pbTotal.increment()
        # print("x")

