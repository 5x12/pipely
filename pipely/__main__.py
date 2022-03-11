import typer
from typing import Optional
import os, pathlib
from pipely.engine.runners import FromPipe, FromClass


app = typer.Typer()

@app.command("from-class")
def cli_from_class(class_path: str, context_path: Optional[str] = None):
    FromClass(class_path, context_path).run()

@app.command("from-pipeline")
def cli_from_pipeline(pipeline_path: str):
    if pathlib.Path(pipeline_path).suffix not in ['.yml', '.yaml']:
        raise Exception(f'Argument {pipeline_path} must be a .yml/.yaml file.')
    if not os.path.exists(pipeline_path):
        raise Exception(f'Cannot find {pipeline_path} at your directory')
    FromPipe(pipeline_path).run()

if __name__ == "__main__":
    app()
