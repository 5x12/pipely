from typing import Optional
import os
from pipely.yamlread.yamlread import yamlRead
from pipely.triggerclass.triggerclass import triggerClass

class Run:
    def __init__(self, config_file: Optional[str] = None, 
                       project_dir: Optional[str] = None,
                       trigger_class: Optional[str] = None):
        
        self.config_file = config_file
        self.project_dir = project_dir
        self.trigger_class = trigger_class

        if (self.config_file is None) & (self.trigger_class is None):
            raise Exception(f'Nothing to do. Please specify either --config_file or --trigger_class. Use ppline --help for more info.')

        if self.project_dir is not None:
            path = self.project_dir+'/'+self.config_file
            if os.path.exists(path)==False:
                raise Exception(f'Cannot find a config .yml/.yaml file at path {path}.')
            execute=yamlRead(dag_path=path)
            execute()             
            
        if self.trigger_class is not None:
            path_to_file, class_to_trigger = self.trigger_class.split(":")
            if os.path.exists(path_to_file)==False:
                raise Exception(f'Cannot find a .py file at path {path_to_file}.')
            execute = triggerClass(path_to_file, class_to_trigger)
            execute()