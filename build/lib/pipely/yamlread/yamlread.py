import yaml
import logging
logging.basicConfig(level=logging.INFO)
logging.info('log level is INFO') 
import copy
import multiprocessing

# from ppline.yamlread.validation.schemes.v1_0 import parse_schema
# from ppline.yamlread.validation.schemes.v1_0 import STATIC_DAG_SCHEMA
# from ppline.utils import deep_update
# from ppline.utils.const import dagmap_consts

class yamlRead(object):
    # def __init__(self, dag_path: str, gitlab: False):
    #     self.pipeline = {}
    #     with open(dag_path, 'r') as inf:
    #         stream = '\n'.join(inf.readlines())
    #     try:
    #         deep_update(self.pipeline, yaml.load(stream, yaml.Loader))
    #     except yaml.YAMLError:
    #         raise Exception("Invalid YAML.")
    
    # def parse_pipeline(self) -> dict:
    #     """Parse a raw user pipeline. Currently just validate the schema.

    #     :param dict pipeline: A raw pipeline passed to Dagestator.
    #     :return dict: The parsed pipeline.
    #     """
    #     self.pipeline= parse_schema(self.pipeline, STATIC_DAG_SCHEMA)

    # def extract_executables(self):
    #     self.commands = [val[dagmap_consts.EXEC_KEYNAME] for val in self.pipeline[dagmap_consts.STEPS_KEYNAME].values()]
    #     self.stages = [val for val in self.pipeline[dagmap_consts.STEPS_KEYNAME].keys()]

    def __init__(self, dag_path: str):
        self.dag_path = dag_path

    def read_yaml(self, file_name: str) -> dict:
        '''
        Reads yaml config file.
        '''
        with open(file_name, "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def make_steps(self, d: dict) -> list:
        '''
        Makes list of lists. Each list represents modules that can be executed in parallel.
        '''
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
        
        
    def get_parsed(self, path_to_class):
        """Parse .
        """
        _file = path_to_class.split(':')[0][:-3].replace('/', '.')
        _class = path_to_class.split(':')[1]
        return _file, _class

    
    def execute(self, script):
        _file, _class = self.get_parsed(script)
        exec(f'from {_file} import {_class}')
        exec(f'c = {_class}()')
        exec(f'c()')

    def __call__(self):
        d = self.read_yaml(self.dag_path)
        steps = self.make_steps(d)

        for step in steps:
            scripts = [d['steps'][x]['exec'] for x in step]
            logging.info(f'{scripts} are in progress')
            process_pool = multiprocessing.Pool(processes = len(step))    
            process_pool.map(execute, scripts)
            logging.info(f'{scripts} done')
