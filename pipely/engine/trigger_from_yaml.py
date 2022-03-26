import os
import copy
import inspect
import importlib.util as importutils
from multiprocessing import Manager

import json
import yaml
from mpire import WorkerPool

from pipely.config.config import logging

from typing import Optional

class YamlTrigger:
    def __init__(self, pipeline_path: str, context_path: Optional[str]):
        """Takes config path and sets the root directory where it exists.
        """
        self.pipeline_path = pipeline_path
        self.context_path = context_path

    @staticmethod
    def read_yaml(path: str) -> dict:
        '''Reads yaml configuration file.
        '''
        with open(path, "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as err:
                print(err)
                return None

    @staticmethod
    def make_steps(d: dict) -> list:
        '''Makes list of lists. Each list represents modules that can be executed in parallel.
        '''
        logging.info(' \t PIPELY is building the pipeline.')
        logging.info(' \t PIPELY is searching for modules that can be executed in parallel.')
        d = d['steps']
        d_new = copy.deepcopy(d)

        done = []
        steps = []

        for key, _ in d.items():
            step = []
            if ('depends_on' not in d[key].keys() or d_new[key]['depends_on'] == set()) and key not in done:
                step.append(key)
                done.append(key)
                for key_new, _ in d_new.items():
                    if key_new != key and key_new not in done:
                        if ('depends_on' not in d_new[key_new].keys() or d_new[key_new]['depends_on'] == set()):
                            step.append(key_new)
                            done.append(key_new)
                        else:
                            d_new[key_new]['depends_on'] = set(d_new[key_new]['depends_on']) - set(done)
            if step != []:
                steps.append(step)
        return steps

    @staticmethod
    def do(context, path_to_class):
        """Executes the class.
        """
        file_name = path_to_class.rsplit(':')[0]
        class_name = path_to_class.rsplit(':')[1]

        spec = importutils.spec_from_file_location("mdl", file_name)
        module = importutils.module_from_spec(spec)
        spec.loader.exec_module(module)
        class_ = getattr(module, class_name)
        instance = class_()
        signature = inspect.signature(instance)
        if len(signature.parameters) == 1:
            instance(context)
        else:
            instance()

        ## [PLACEHOLDER]
        ## respond upon completion for dashboard
        ##

    def execute(self):
        d = self.read_yaml(self.pipeline_path)
        steps = self.make_steps(d)
        pipe_root = os.path.dirname(self.pipeline_path)
        logging.info(' \t PIPELY has picked up the tasks.')
        context = Manager().dict()
        if self.context_path:
            with open(self.context_path, 'r') as fp:
                    context.update(json.load(fp))
        for step in steps:
            scripts = [
                os.path.join(pipe_root, d['steps'][x]['exec'])
                for x in step]
            logging.info(f' --> NEXT IN PROGRESS: Step(s) {step} \n \t \t \t \t Script(s) {scripts}')
            with WorkerPool(n_jobs = len(step)) as process_pool:
                process_pool.set_shared_objects(context)
                process_pool.map(self.do, scripts)
                logging.info(f' --> DONE: Script(s) {scripts} finished.')
