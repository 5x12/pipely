import importlib.util as importutils
import os

class ClassTrigger:
    def __init__(self, class_path: str):
        self.path_to_file = class_path.rsplit(":")[0]
        self.class_to_trigger = class_path.rsplit(":")[1]
        if not os.path.exists(self.path_to_file):
            raise Exception(f'Cannot find {self.path_to_file}.')

    def execute(self):
        spec = importutils.spec_from_file_location("mdl", self.path_to_file)
        module = importutils.module_from_spec(spec)
        spec.loader.exec_module(module)
        class_ = getattr(module, self.class_to_trigger)
        instance = class_()
        instance()