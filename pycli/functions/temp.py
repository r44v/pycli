import subprocess
import tempfile
import shutil
import uuid
import pathlib

def make_temp_project():
    temp_dir = pathlib.Path(tempfile.mkdtemp())
    path = shutil.which("code")
    loc_data = temp_dir / "data.txt"
    loc_code = temp_dir / "main.py"
    template = f"""## This is a template file
import pathlib
import json
import re

INPUT_DATA = '{loc_data.absolute().as_posix()}'
data = pathlib.Path(INPUT_DATA).read_text(encoding='utf-8')

print(json.dumps(data, indent=4))
"""
    loc_code.write_text(template, encoding="utf-8")
    loc_data.touch()
    subprocess.Popen([path, '-n', loc_code.parent.as_posix()])