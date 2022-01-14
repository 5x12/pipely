import argparse, os, pathlib
from typing import Optional
from pipely.engine.run import Run

def _arg_config_file(arg):
    if pathlib.Path(arg).suffix not in ['.yml', '.yaml']:
        raise Exception(f'Argument {arg} must be a .yml/.yaml file.')
    if os.path.exists(arg)==False:
        raise Exception(f'Cannot find {arg} at your directory')
    return arg

parser = argparse.ArgumentParser()
parser.add_argument('--trigger_class', '-tc', default=None, help='Path to class to trigger (in the form of "to/the/file.py:TestClass. TestClass should have a __call__ method")')
parser.add_argument('--config_file', '-f', type=_arg_config_file, default=None, help='Name of pipeline configuration .yml/.yaml file')
# parser.add_argument('-gitlab', action='store_true', help='Specify if you want to generate .gitlab-ci file.yaml')

args = parser.parse_args()
Run(config_file=args.config_file, trigger_class=args.trigger_class)