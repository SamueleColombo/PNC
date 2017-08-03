import numpy as np
import os
import pandas as pd
import re
import sys
import subprocess
import tensorflow as tf

from tensorflow.contrib.learn.python.learn.estimators import run_config
from tensorflow.contrib import learn

from pnc.trainer.estimator import  generate_estimator_fn
from pnc.trainer.__main__ import main as train
from pnc.trainer.model import model_fn
from pnc.trainer.model import generate_model_fn
from pnc.trainer.experimenter import generate_input_fn

CLASS = ['N', 'A', 'O', 'S']

def main():

    args = {}

    predictions = {}

    # Iterate all over the classes.
    for c in CLASS:
        # Call the subprocess for the current class.
        args[c] = train(['', '--config', '../PNC-data/PNC-configs/config-{}.cfg'.format(c), '--train', 'True'])

    # Iterate all over the classes.
    for c in CLASS:
        # Restore the model to make predictions.
        estimator = tf.estimator.Estimator(
            model_fn=generate_model_fn(
                hidden_units=args[c].hidden_units,
                dropout=args[c].dropout,
                learning_rate=args[c].learning_rate,
                weights=args[c].weights,
            ),
            # Set the same configuration used in the training process.
            config=run_config.RunConfig(model_dir=args[c].job_dir)
        )

        # Create the prediction function to train the global neural network.
        predict_input_fn = lambda: generate_input_fn(
            args[c].train_files,
            epochs=1,
            batch_size=args[c].train_batch_size,
            mapping=args[c].mapping,
            shuffle=False,
            defaults=args[c].defaults,
            features=args[c].features,
        )

        # Save the prediction of this neural network.
        predictions[c] = list([p['classes'] for p in estimator.predict(input_fn=predict_input_fn)])

    A = [np.asarray(v, dtype=int)[:-1] for k,v in predictions.items()]

    data = pd.read_csv(args['N'].train_files).as_matrix().T

    predictions = []

    # Previous data except the target.
    for d in data[:-1]:
        predictions.append(np.asarray(d, dtype=str))

    # Data from the predictions.
    for p in A:
        predictions.append(p)

    # Target features
    predictions.append(np.asarray(data[-1], dtype=str))

    predictions = np.array(predictions)

    predictions = predictions.T

    B = pd.DataFrame(A)

    with open(os.path.join(os.getcwd(), 'PNC-data\\PNC-inputs\\predict-1.csv'), 'w') as f:
        for p in predictions:
            # Save the prediction in the predict file.
            # np.savetxt(f, [a1 for a1 in a], delimiter=',', fmt='%s')
            # B.to_csv(f)
            f.write(','.join(np.asarray(p, dtype=str)) + '\n')

    global_train_input_fn = lambda: generate_input_fn(
        os.path.join(os.getcwd(), 'PNC-data\\PNC-inputs\\predict-1.csv'),
        epochs=1000,
        batch_size=10000,
        mapping={0: 0, 1: 1, 2: 2, 3: 3},
        shuffle=True,
        defaults=['', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] + [0, 0, 0, 0] + [0],
        features=['FN', 'SS', 'SN', 'SL','NS', 'NN', 'NL', 'LS', 'LN', 'LL'] + CLASS + ['FT'],
    )

    # Restore the model to make predictions.
    estimator = tf.estimator.Estimator(
        model_fn=generate_model_fn(
            hidden_units=[10, 20, 10],
            learning_rate=0.01,
            weights=[1.0, 1.0],
        ),
        # Set the same configuration used in the training process.
        config=run_config.RunConfig(model_dir='../PNC-data/PNC-outputs/DNN')
    )

    estimator.train(input_fn=global_train_input_fn)



if __name__ == '__main__':
    # Run the main function and halt itself.
    sys.exit(main())