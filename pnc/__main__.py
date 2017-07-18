import argparse
import ast
import configparser
import os
import shutil
import sys

import tensorflow as tf

from pnc.trainer import run

SECTIONS = [
    'Settings',
    'Parameters',
    'Hyperparameters',
    'Train',
    'Eval',
    'Predict',
    'Others',
]

def main(argv=None):
    """

    :param argv:
    :return:
    """

    if not argv:
        # Set the argv with the default arguments.
        argv = sys.argv

    # Create the parser for the configuration file.
    conf_parser = argparse.ArgumentParser(
        # Printed with -h or --help.
        description=__doc__,
        # Fit with the description format.
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # Turn off the help page.
        add_help=False
    )

    # Add the configuration file argument.
    conf_parser.add_argument('-c', '--config', help='', metavar='FILE')
    # Parse only the configuration argument (all the other args will be saved in the `others` variable).
    args, others = conf_parser.parse_known_args()

    # Create the default dictionary (it will be eventually updated from the configuration file information).
    defaults = {
        'verbosity': None,
        'job_dir': None,
        'dropout': 0,
        'learning_rate': 0.0,
        'hidden_units': [],
        'epochs': 0,
        'train': False,
        'train_files': [],
        'train_steps': None,
        'train_batch_size' : None,
        'eval': False,
        'eval_files': [],
        'eval_steps': None,
        'eval_batch_size': None,
        'predict': False,
        'mapping': None,
    }

    if args.config:
        # Create the parser for the content of the configuration file.
        config = configparser.ConfigParser()
        # Read the configuration file.
        config.read([args.config])

        # Iterate all over the sections in the configuration file.
        for section in SECTIONS:

            # Get the (key, value) pair.
            for key, value in config.items(section):

                #
                try:
                    # Cast the value using a lexical evaluation.
                    value = ast.literal_eval(value)
                except:
                    # It raises a lot of exception.
                    pass

                # Update the default values in the current section.
                defaults.update({key: value})

    # Create the parser for the others argument.
    arg_parser = argparse.ArgumentParser(
        # Inherit options from the conf_parser.
        parents=[conf_parser]
    )

    # Set the default values.
    arg_parser.set_defaults(**defaults)

    arg_parser.add_argument('--verbosity', choices=['DEBUG', 'INFO', 'ERROR', 'FATAL', 'INFO', 'WARN'])
    arg_parser.add_argument('--job-dir', type=str)
    arg_parser.add_argument('--transform')
    arg_parser.add_argument('--dropout', type=float)
    arg_parser.add_argument('--learning-rate', type=float)
    arg_parser.add_argument('--hidden-units')
    arg_parser.add_argument('--epochs')
    arg_parser.add_argument('--train', type=bool)
    arg_parser.add_argument('--train-files')
    arg_parser.add_argument('--train-steps')
    arg_parser.add_argument('--train-batch-size')
    arg_parser.add_argument('--eval', type=bool)
    arg_parser.add_argument('--eval-files')
    arg_parser.add_argument('--eval-steps')
    arg_parser.add_argument('--eval-batch-size')
    arg_parser.add_argument('--predict', type=bool)
    arg_parser.add_argument('--mapping')

    # Parse the other arguments.
    args = arg_parser.parse_args(others)

    # Set python level verbosity
    tf.logging.set_verbosity(args.verbosity)
    # Set C++ Graph Execution level verbosity
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = str(tf.logging.__dict__[args.verbosity] / 10)

    # Run the trainer.
    run(args)

if __name__ == '__main__':
    # Run the main function and halt itself.
    sys.exit(main())






