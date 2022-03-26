import typer
from typing import Optional
import os, pathlib

from pipely.engine import YamlTrigger, ClassTrigger
from pipely.config.config import logo

app = typer.Typer()

@app.command("from-class")
def cli_from_class(class_path: str, context_path: Optional[str] = None):
    print(logo)
    ClassTrigger(class_path, context_path).execute()

@app.command("from-pipeline")
def cli_from_pipeline(pipeline_path: str, context_path: Optional[str] = None):
    if pathlib.Path(pipeline_path).suffix not in ['.yml', '.yaml']:
        raise Exception(f'Argument {pipeline_path} must be a .yml/.yaml file.')
    if not os.path.exists(pipeline_path):
        raise Exception(f'Cannot find {pipeline_path} at your directory')
    print(logo)
    YamlTrigger(pipeline_path, context_path).execute()

if __name__ == "__main__":
    app()
