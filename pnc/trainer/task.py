from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import pandas as pd
import tensorflow as tf

from tensorflow.contrib import learn
from tensorflow.contrib import layers
from tensorflow.contrib.learn.python.learn import learn_runner
from tensorflow.contrib.learn.python.learn.estimators import run_config
from tensorflow.contrib.training.python.training import hparam

from experimenter import generate_experimenter_fn
from estimator import generate_estimator_fn
from experimenter import generate_input_fn
from model import generate_model_fn

def run(args):

    learn_runner.run(
        generate_experimenter_fn(
            train_steps=args.train_steps,
            eval_steps=args.eval_steps,
        ),
        # The configuration of the environment.
        run_config=run_config.RunConfig(model_dir=args.job_dir),
        # Set the array of the hyper-parameters.
        # TODO: Use only the hyper-parameters from the configuration file.
        hparams=hparam.HParams(**args.__dict__),
        # Choose the schedule (it's like a washing machine program).
        # schedule=schedule
    )

    # features = args.features.copy()
    #
    # features.remove('FT')
    # features.remove('FN')
    #
    # # Create the estimator.
    # estimator = learn.DNNClassifier(
    #     feature_columns=[layers.real_valued_column(k) for k in features],
    #     n_classes=2,
    #     hidden_units=args.hidden_units,
    #     activation_fn=tf.nn.relu,
    #     dropout=args.dropout,
    #     optimizer=tf.train.GradientDescentOptimizer(learning_rate=args.learning_rate),
    #     config=run_config.RunConfig(model_dir=args.job_dir)
    # )
    #
    # # Create the training function.
    # training_fn = lambda: generate_input_fn(
    #     args.train_files,
    #     epochs=args.epochs,
    #     batch_size=args.train_batch_size,
    #     mapping=args.mapping,
    #     shuffle=True,
    #     defaults=args.defaults,
    #     features=args.features,
    # )
    #
    # # Train the model.
    # estimator.fit(input_fn=training_fn, steps=2000)
    #
    # # Create the evaluating function.
    # evaluating_fn = lambda: generate_input_fn(
    #     args.eval_files,
    #     batch_size=args.eval_batch_size,
    #     mapping=args.mapping,
    #     shuffle=False,
    #     defaults=args.defaults,
    #     features=args.features,
    # )
    #
    # # Evaluate the model.
    # estimator.evaluate(input_fn=evaluating_fn, steps=1)
    #

  