from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

from tensorflow.contrib import layers
from tensorflow.python.estimator.model_fn import ModeKeys
from tensorflow.contrib.learn import ModelFnOps
from tensorflow.contrib import metrics
from tensorflow.contrib import framework

def generate_model_fn(hidden_units=[10, 20, 10],
                      dropout=0.3,
                      learning_rate=0.5,
                      weights=[1.0, 1.0]):
    """

    :param hidden_units:
    :param dropout:
    :param learning_rate:
    :param num_class:
    :return:
    """

    def _model_fn(features, labels, mode):
        """

        :param features:
        :param labels:
        :param mode:
        :return:
        """

        # Pop the name of the signal.
        if 'FN' in features:
            names = features.pop('FN')

        if 'FT' in features:
            labels = features.pop('FT')


        # Define the type of the inputs (they are all numeric).
        columns = [layers.real_valued_column(key) for key, value in features.items()]
        #
        inputs = layers.input_from_feature_columns(features, columns)

        # Declare the hidden_layers variable.
        hidden_layers = None

        # Iterate all over the hidden units.
        for unit in hidden_units:
            # Create a new hidden layer.
            hidden_layers = tf.layers.dense(
                inputs=inputs if hidden_layers is None else hidden_layers,
                activation=tf.nn.relu,
                units=unit,
            )

        # Create a dropout layer.
        dropout_layer = layers.dropout(
            inputs=hidden_layers,
            keep_prob=1.0 - dropout
        )

        # Create the logits layer.
        logits = tf.layers.dense(
            inputs=dropout_layer,
            activation=None,
            units=2
        )

        if mode in (ModeKeys.PREDICT, ModeKeys.EVAL):
            # Calculate the probabilities.
            probabilities = tf.nn.softmax(logits)
            # And their indexes.
            predictions = tf.argmax(logits, 1)

        if mode in (ModeKeys.EVAL, ModeKeys.TRAIN):
            # Convert the labels in the one_hot format.
            onehot_labels = tf.one_hot(indices=labels, depth=2)
            # Define the class weights.
            class_weights = tf.constant(weights)
            # Deduce weights for batch samples based on their true label.
            reduced_weights = tf.reduce_sum(class_weights * onehot_labels, axis=1)
            # Compute your (unweighted) softmax cross entropy loss.
            unweighted_losses = tf.nn.softmax_cross_entropy_with_logits(labels=onehot_labels, logits=logits)
            # Apply the weights, relying on broadcasting of the multiplication.
            weighted_losses = unweighted_losses * reduced_weights
            # Reduce the result to get your final loss.
            loss = tf.reduce_mean(weighted_losses)

        if mode == ModeKeys.PREDICT:

            # Convert predicted_indices back into strings
            predictions = {
                'classes': predictions,
                'scores': probabilities,
            }

            # export_outputs = {
            #     'prediction': tf.estimator.export.PredictOutput(predictions)
            # }

            # return tf.estimator.EstimatorSpec(
            #     mode=mode,
            #     predictions=predictions,
            #     # export_outputs=export_outputs,
            # )

            return tf.estimator.EstimatorSpec(
                mode=mode,
                predictions=predictions,
            )

        if mode == ModeKeys.TRAIN:
            # Define the training rule.
            train_op = layers.optimize_loss(
                loss=loss,
                global_step=framework.get_global_step(),
                learning_rate=learning_rate,
                optimizer='SGD'
            )

            return tf.estimator.EstimatorSpec(
                mode=mode,
                loss=loss,
                train_op=train_op
            )

        if mode == ModeKeys.EVAL:

            # Define the metrics to show up in the evaluation process.
            eval_metric_ops = {
                'accuracy' : metrics.streaming_accuracy(predictions=predictions, labels=labels),
                'auroc' : metrics.streaming_auc(predictions=predictions, labels=labels),
                'recall': metrics.streaming_recall(predictions=predictions, labels=labels),
                'precision': metrics.streaming_precision(predictions=predictions, labels=labels),
                'TP': metrics.streaming_true_positives(predictions=predictions, labels=labels),
                'FN': metrics.streaming_false_negatives(predictions=predictions, labels=labels),
                'FP': metrics.streaming_false_positives(predictions=predictions, labels=labels),
                'TN': metrics.streaming_true_negatives(predictions=predictions, labels=labels),
                #'gaccuracy' : metrics.streaming_accuracy(predictions=GP, labels=GL)
            }

            return tf.estimator.EstimatorSpec(
                mode=mode,
                predictions=predictions,
                loss=loss,
                eval_metric_ops=eval_metric_ops
            )


    return _model_fn


def model_fn(features, labels, mode):
    """

    :param features:
    :param labels:
    :param mode:
    :return:
    """

    # Pop the name of the signal.
    if 'FN' in features:
        names = features.pop('FN')

    if 'FT' in features:
        labels = features.pop('FT')


    # Define the type of the inputs (they are all numeric).
    columns = [layers.real_valued_column(key) for key, value in features.items()]
    #
    inputs = layers.input_from_feature_columns(features, columns)

    # Declare the hidden_layers variable.
    hidden_layers = None

    # Iterate all over the hidden units.
    for unit in [10, 20, 10]:
        # Create a new hidden layer.
        hidden_layers = tf.layers.dense(
            inputs=inputs if hidden_layers is None else hidden_layers,
            activation=tf.nn.relu,
            units=unit,
        )

    # Create a dropout layer.
    dropout_layer = layers.dropout(
        inputs=hidden_layers,
        keep_prob=1.0 - 0.2
    )

    # Create the logits layer.
    logits = tf.layers.dense(
        inputs=dropout_layer,
        activation=None,
        units=2
    )

    if mode in (ModeKeys.PREDICT, ModeKeys.EVAL):
        # Calculate the probabilities.
        probabilities = tf.nn.softmax(logits)
        # And their indexes.
        predicted_classes = tf.argmax(probabilities, 1)

    if mode in (ModeKeys.EVAL, ModeKeys.TRAIN):
        # Convert the labels in the one_hot format.
        onehot_labels = tf.one_hot(indices=labels, depth=2)
        # Define the class weights.
        class_weights = tf.constant([1.0, 1.0])
        # Deduce weights for batch samples based on their true label.
        reduced_weights = tf.reduce_sum(class_weights * onehot_labels, axis=1)
        # Compute your (unweighted) softmax cross entropy loss.
        unweighted_losses = tf.nn.softmax_cross_entropy_with_logits(labels=onehot_labels, logits=logits)
        # Apply the weights, relying on broadcasting of the multiplication.
        weighted_losses = unweighted_losses * reduced_weights
        # Reduce the result to get your final loss.
        loss = tf.reduce_mean(weighted_losses)

    if mode == ModeKeys.PREDICT:

        # Convert predicted_indices back into strings
        predictions = {
            # TODO: Why prediction needs labels?
            'classes': tf.gather(labels, predicted_classes),
            # TODO: Add axis=1 to reduce_max.
            'scores': tf.reduce_max(input_tensor=predicted_classes)
        }

        export_outputs = {
            'prediction': tf.estimator.export.PredictOutput(predictions)
        }

        return tf.estimator.EstimatorSpec(
            mode=mode,
            predictions=predictions,
            export_outputs=export_outputs,
        )

    if mode == ModeKeys.TRAIN:
        # Define the training rule.
        train_op = layers.optimize_loss(
            loss=loss,
            global_step=framework.get_global_step(),
            learning_rate=0.5,
            optimizer='SGD'
        )

        return tf.estimator.EstimatorSpec(
            mode=mode,
            loss=loss,
            train_op=train_op
        )

    if mode == ModeKeys.EVAL:

        # Define the metrics to show up in the evaluation process.
        eval_metric_ops = {
            'accuracy' : metrics.streaming_accuracy(predictions=predicted_classes, labels=labels),
            'auroc' : metrics.streaming_auc(predictions=predicted_classes, labels=labels),
            'recall': metrics.streaming_recall(predictions=predicted_classes, labels=labels),
            'precision': metrics.streaming_precision(predictions=predicted_classes, labels=labels),
            'TP': metrics.streaming_true_positives(predictions=predicted_classes, labels=labels),
            'FN': metrics.streaming_false_negatives(predictions=predicted_classes, labels=labels),
            'FP': metrics.streaming_false_positives(predictions=predicted_classes, labels=labels),
            'TN': metrics.streaming_true_negatives(predictions=predicted_classes, labels=labels),
            #'gaccuracy' : metrics.streaming_accuracy(predictions=GP, labels=GL)
        }

        return tf.estimator.EstimatorSpec(
            mode=mode,
            predictions=predicted_classes,
            loss=loss,
            eval_metric_ops=eval_metric_ops
        )









