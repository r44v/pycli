import os
import pathlib
import tempfile
import shutil


def read_env() -> "dict[str, str]":
    env_file = pathlib.Path(__file__).parent.parent.joinpath(".env")
    
    if not env_file.exists():
        return
    
    environment_variables = dict()
    
    with env_file.open("r", encoding="utf-8") as fs:
        env_vars = fs.readlines()
    for env_var in env_vars:
        env_var = env_var.strip()
        if env_var.startswith("#") or not env_var:
            continue
        key, value = env_var.split("=")
        environment_variables[key.strip()] = value.strip()
    
    return environment_variables

def load_env():
    os.environ.update(read_env())

def print_with_glow(content: str):
    """
    Outputs content with glow if glow is installed.

    Glow is a cli markdown renderer

    https://github.com/charmbracelet/glow
    """
    if not shutil.which("glow"):
        print(content)
        return

    f = tempfile.TemporaryFile(delete=False)
    try:
        f.write(content.encode('utf-8'))
        f.close()
        os.system(f"glow {f.name}")
    finally:
        pathlib.Path(f.name).unlink(missing_ok=True)