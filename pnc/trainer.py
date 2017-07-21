from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pandas as pd
import tensorflow as tf

from tensorflow.contrib.learn.python.learn import learn_runner
from tensorflow.contrib.learn.python.learn.estimators import run_config
from tensorflow.contrib.training.python.training import hparam

from experimenter import generate_experimenter_fn
from estimator import generate_estimator_fn
from experimenter import generate_input_fn

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



    classifier = generate_estimator_fn(
        config=run_config.RunConfig(model_dir=args.job_dir),
        hidden_units=args.hidden_units,
        dropout=args.dropout,
        features=args.features,
    )

    d = pd.read_csv(args.train_files).as_matrix()


    def train_fn():
        x = dict(zip(args.features, [t for t in d.T]))
        x.pop('FN')
        y = x.pop('FT')
        y = tf.constant(y.tolist())

        for k,v in x.items():
            x[k] = tf.constant(v.tolist())


        return x,y


    classifier.fit(input_fn=train_fn, steps=1000)

    # classifier.fit(input_fn=generate_input_fn(
    #     args.train_files,
    #     shuffle=True,
    #     batch_size=args.train_batch_size,
    #     epochs=1000,
    #     mapping=args.mapping,
    #     features=args.features,
    #     defaults=args.defaults,
    # ))
    #
    # learn_runner.run(
    #     generate_estimator_fn(
    #         train_steps=args.train_steps,
    #         eval_steps=args.eval_steps,
    #     ),
    #     # The configuration of the environment.
    #     run_config=run_config.RunConfig(model_dir=args.job_dir),
    #     # Set the array of the hyper-parameters.
    #     # TODO: Use only the hyper-parameters from the configuration file.
    #     hparams=hparam.HParams(**args.__dict__),
    #     # Choose the schedule (it's like a washing machine program).
    #     # schedule=schedule
    # )
