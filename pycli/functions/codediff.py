import subprocess
import tempfile
import shutil

def codediff():
    _, file_a = tempfile.mkstemp()
    _, file_b = tempfile.mkstemp()
    path = shutil.which("code")
    subprocess.Popen([path, '-n', '--diff', file_a, file_b])