#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jian Guo
"""
import argparse
import os
import tensorflow as tf
import numpy as np
import pandas as pd
from tqdm import tqdm
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image


if  __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-m', '--mode', required=True)
    # io_args = parser.parse_args()
    # mode = io_args.mode
    
    def create_model():
        cnn = tf.keras.models.Sequential()
        cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu', input_shape=[64, 64, 1]))
        cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
        cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu'))
        cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
        cnn.add(tf.keras.layers.Flatten())
        cnn.add(tf.keras.layers.Dense(units=128, activation='relu'))
        cnn.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))
        cnn.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
        return cnn
        
    # if mode == 'test':
        import timeit

        # start = timeit.default_timer()
    # load cnn
    cnn = create_model()
    cnn.load_weights('../classifier/model/model')
    # predict
    entries = os.listdir('../classifier/EICplots')
    res = []
    for entry in tqdm(entries):
        if entry.endswith('.png'):
            path = '../classifier/EICplots/' + entry
            test_image = tf.keras.utils.load_img(path, color_mode='grayscale', target_size = (64, 64))
            test_image = tf.keras.utils.img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis = 0)
            result = cnn.predict(test_image, verbose=0).squeeze()
            b = False
            if result >= 0.5:
                b = True
            res.append(np.array([entry, result, b]))
    res = np.asarray(res)
    df = pd.DataFrame(res)
    df.columns = ['image', 'score', 'prediction']
    df.to_csv('../output/PredictionOutcome.csv', index=False)
    # tf.saved_model.save(cnn)
    # tf.train.Checkpoint(cnn).restore(save_path='../classifier/model/model').expect_partial()
        # stop = timeit.default_timer()
        # print('Time: ', stop - start)