from pipely.config.config import logging
from mpire import WorkerPool
import yaml, copy, sys, os

class triggerYaml(object):
    def __init__(self, path: str):
        """Takes config path and sets the root directory where it exists.
        """
        self.path = path
        try:
            print(sys.path.append(str(os.path.abspath(f'{path}/..'))))
            sys.path.append(str(os.path.abspath(f'{path}/..')))
        except OSError as err:
            print(err)

    def read_yaml(self, path: str) -> dict:
        '''Reads yaml configuration file.
        '''
        with open(path, "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as err:
                print(err)

    def make_steps(self, d: dict) -> list:
        '''Makes list of lists. Each list represents modules that can be executed in parallel.
        '''
        logging.info(f' \t PIPELY is building the pipeline.')
        logging.info(f' \t PIPELY is searching for modules that can be executed in parallel.')
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
         
    def _get_parsed(self, path_to_class):
        """Parses the class and path to the file from "path_to_file/file.py:Class".
        """
        _file = path_to_class.split(':')[0][:-3].replace('/', '.')
        _class = path_to_class.split(':')[1]
        return _file, _class
    
    def execute(self, path_to_class):
        """Executes the class.
        """
        _file, _class = self._get_parsed(path_to_class)
        exec(f'from {_file} import {_class}')
        exec(f'c = {_class}()')
        exec(f'c()')

        ## [PLACEHOLDER]
        ## respond upon completion for dashboard
        ##

    def __call__(self):
        d = self.read_yaml(self.path)
        steps = self.make_steps(d)

        logging.info(f' \t PIPELY has picked up the tasks.')
        for step in steps:
            scripts = [d['steps'][x]['exec'] for x in step]
            logging.info(f' --> NEXT IN PROGRESS: Step(s) {step} \n \t \t \t \t Script(s) {scripts}')
            process_pool = WorkerPool(n_jobs = len(step))
            process_pool.map(self.execute, scripts)
            logging.info(f' --> DONE: Script(s) {scripts} finished.')