from tensorflow.contrib.learn.python.learn import learn_runner
from tensorflow.contrib.learn.python.learn.estimators import run_config
from tensorflow.contrib.training.python.training import hparam

from experimenter import generate_experimenter_fn

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
