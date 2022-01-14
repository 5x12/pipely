class triggerClass(object):
    def __init__(self, path_to_file: str, class_to_trigger: str):
        self.path_to_file = path_to_file
        self.class_to_trigger = class_to_trigger
        
    def executor(self): 
        _file=self.path_to_file.split(':')[0][:-3].replace('/', '.')
        _class = self.class_to_trigger
        
        exec(f'from {_file} import {_class}')
        exec(f'c = {_class}()')
        exec(f'c()')

    def __call__(self):
        self.executor()