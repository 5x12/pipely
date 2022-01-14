import os
from typing import Optional
from pipely.engine.triggeryaml.triggeryaml import triggerYaml
from pipely.engine.triggerclass.triggerclass import triggerClass
from pipely.config.config import logo

class Run:
    def __init__(self, config_file: Optional[str] = None, 
                       trigger_class: Optional[str] = None):
        
        self.config_file = config_file
        self.trigger_class = trigger_class
        print(logo)

        if (self.config_file is None) & (self.trigger_class is None):
            raise Exception(f'Nothing to do. Please specify either --config_file or --trigger_class. Use pipely --help for more info.')

        if (self.config_file is not None) & (self.trigger_class is not None):
            raise Exception(f'Too many arguments. Choose either  --trigger_class or --config_file. Use pipely --help for more info.')

        if (self.config_file is not None):
            path = self.config_file
            execute=triggerYaml(path=path)
            execute()
            
        if self.trigger_class is not None:
            path_to_file, class_to_trigger = self.trigger_class.split(":")
            if os.path.exists(path_to_file)==False:
                raise Exception(f'Cannot find a .py file at path {path_to_file}.')
            execute = triggerClass(path_to_file, class_to_trigger)
            execute()