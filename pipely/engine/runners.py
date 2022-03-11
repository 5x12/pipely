
import os
from pipely.engine import YamlTrigger, ClassTrigger
from pipely.config.config import logo

class FromPipe:
    def __init__(self, pipe_file: str) -> None:
        self.pipe_file = pipe_file

    def run(self):
        print(logo)
        path = self.pipe_file
        YamlTrigger(path=path).execute()

class FromClass:
    def __init__(self, class_path: str) -> None:
        self.path_to_file, self.class_to_trigger = self.class_path.rsplit(":")

    def run(self):
        print(logo)
        path_to_file = self.path_to_file
        class_to_trigger = self.class_to_trigger
        if not os.path.exists(path_to_file):
            raise Exception(f'Cannot find {path_to_file}.')
        ClassTrigger(path_to_file, class_to_trigger).execute()
