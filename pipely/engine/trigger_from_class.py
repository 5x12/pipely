import importlib.util as importutils
import os
from typing import Optional
import json
import inspect

class ClassTrigger:
    def __init__(self, class_path: str, context_path: Optional[str]):
        self.path_to_file = class_path.rsplit(":")[0]
        self.class_to_trigger = class_path.rsplit(":")[1]
        self.context_path = context_path
        if not os.path.exists(self.path_to_file):
            raise Exception(f'Cannot find {self.path_to_file}.')
        if self.context_path and not os.path.exists(self.context_path):
            raise Exception(f'Cannot find {self.context_path}.')

    def execute(self, context=None):
        spec = importutils.spec_from_file_location("mdl", self.path_to_file)
        module = importutils.module_from_spec(spec)
        spec.loader.exec_module(module)
        class_ = getattr(module, self.class_to_trigger)
        instance = class_()
        signature = inspect.signature(instance)
        if len(signature.parameters) == 1:
            with open(self.context_path, 'r') as fp:
                context = json.load(fp)
            instance(context)
        else:
            instance()