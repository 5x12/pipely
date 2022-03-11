
import os
from pipely.engine import YamlTrigger, ClassTrigger
from pipely.config.config import logo

class FromPipe:
    def __init__(self, pipe_file: str) -> None:
        self.pipe_file = pipe_file

    def run(self):
        print(logo)
        YamlTrigger(self.pipe_file).execute()

class FromClass:
    def __init__(self, class_path: str) -> None:
        self.class_path = class_path

    def run(self):
        print(logo)
        ClassTrigger(self.class_path).execute()
