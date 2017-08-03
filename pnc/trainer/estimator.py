from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

from tensorflow.contrib import learn
from tensorflow.contrib import layers


def generate_feature_engineering_fn(features, labels):

    # Pop the name of the signal.
    # names = features.pop('FN')
    #
    # # Define the type of the inputs (they are all numeric).
    # columns = [layers.real_valued_column(key) for key, value in features.items()]
    #
    # inputs = layers.input_from_feature_columns(features, columns)

    # Return the processed data for the DNN classifier.
    return features, labels

def generate_estimator_fn(config, dropout, features, hidden_units, learning_rate=0.5):

    # # Create a copy.
    columns = features.copy()
    # Remove the name column.
    columns.remove('FN')
    # Remove the target column.
    columns.remove('FT')

    # Create the DNN classifier.
    return learn.DNNClassifier(
        # Set the input data structure.
        feature_columns=[layers.real_valued_column(key) for key in columns],
        # Just 0 and 1.
        n_classes=2,
        # The array of the inputs for each hidden unit.
        hidden_units=hidden_units,
        # The dropout ratio.
        dropout=dropout,
        # Takes features and labels which are the output of input_fn and returns features and labels which will be fed into the model
        #feature_engineering_fn=generate_feature_engineering_fn,
        # The default settings.
        config=config,
    )





