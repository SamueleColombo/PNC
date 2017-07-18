import multiprocessing

import tensorflow as tf
from tensorflow.contrib import learn

from model import generate_model_fn

DEFAUTS = {
    'mapping': {0: 0, 1: 1, 2: 2, 3: 3},
    'features': ['FN', 'F1', 'F2', 'F3','F4', 'FT'],
    'values': ['', 0.0, 0.0, 0.0, 0.0, 0],
}

def generate_input_fn(files,
                      shuffle,
                      batch_size,
                      epochs=None,
                      mapping=DEFAUTS['mapping'],
                      features=DEFAUTS['features'],
                      defaults=DEFAUTS['values']):
    """

    :param files:
    :param shuffle:
    :param batch_size:
    :param epochs:
    :param mapping:
    :param features:
    :param defaults:
    :return:
    """

    # Initialize the stream of files.
    queue = tf.train.string_input_producer(
        # TODO: Put the file in a real array.
        [files],
        num_epochs=epochs,
        shuffle=shuffle
    )

    # Create the file reader.
    reader = tf.TextLineReader(skip_header_lines=False)
    # Returns up to num_records (key, value pairs) produced by a reader.
    _, rows = reader.read_up_to(queue, num_records=batch_size)


    # Decode the data (the missing data are replaced using the default values).
    columns = tf.decode_csv(rows, [[d] for d in defaults])

    # Create a dictionary using the columns name and the data previously decoded.
    features = dict(zip(features, columns))

    # Check if the class need to be mapped:
    if mapping:
        # Map the class using the map argument.
        features['FT'] = tf.map_fn(lambda x: mapping[x] if x in mapping else x, features['FT'])


    if shuffle:
        features = tf.train.shuffle_batch(
            tensors=features,
            batch_size=batch_size,
            min_after_dequeue=2 * batch_size + 1,
            capacity=batch_size * 10,
            num_threads=multiprocessing.cpu_count(),
            enqueue_many=True,
            allow_smaller_final_batch=True
        )
    else:
        features = tf.train.batch(
            tensors=features,
            batch_size=batch_size,
            capacity=batch_size * 10,
            num_threads=multiprocessing.cpu_count(),
            enqueue_many=True,
            allow_smaller_final_batch=True
        )

    # Get the label from the features dict.
    label = features.pop('FT')

    # Return both the tensors of the features and the labels.
    return features, label


def generate_experimenter_fn(**args):
    """
    Create the Experimenter function.

    :param args:
    :return:
    """

    def _experimenter_fn(run_config, hparams):
        """

        :param run_config:
        :param hparams:
        :return:
        """

        # Create the training function.
        training_fn = lambda: generate_input_fn(
            hparams.train_files,
            epochs=hparams.epochs,
            batch_size=hparams.train_batch_size,
            mapping=hparams.mapping,
            shuffle=True,
            defaults=hparams.defaults,
            features=hparams.features,
        )

        # Create the evaluating function.
        evaluating_fn = lambda: generate_input_fn(
            hparams.eval_files,
            batch_size=hparams.eval_batch_size,
            mapping=hparams.mapping,
            shuffle=False,
            defaults=hparams.defaults,
            features=hparams.features,
        )

        # Return the Experiment.
        return learn.Experiment(
            tf.estimator.Estimator(
                generate_model_fn(
                    num_signals=2523,
                    learning_rate=hparams.learning_rate,
                    hidden_units=hparams.hidden_units,
                    dropout=hparams.dropout,
                    weights=hparams.weights,
                ),
                config=run_config,
            ),
            train_input_fn=training_fn,
            eval_input_fn=evaluating_fn,
            **args
        )

    return _experimenter_fn
