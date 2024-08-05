import os
import pathlib
import tempfile
import shutil
import subprocess


def read_env() -> "dict[str, str]":
    env_file = pathlib.Path(__file__).parent.parent.joinpath(".env")

    if not env_file.exists():
        return dict()

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
        f.write(content.encode("utf-8"))
        f.close()
        os.system(f"glow {f.name}")
    finally:
        pathlib.Path(f.name).unlink(missing_ok=True)


def docker_deamon_available():
    """
    Returns True if docker daemon is available
    """
    try:
        subprocess.run(["docker", "ps"], capture_output=True)
        return True
    except Exception as e:
        print(e)
        return False


def get_ports_used_by_docker():
    """
    Returns a list of ports used by docker containers
    """

    ports = []
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Ports}}"], capture_output=True
        )
        for line in result.stdout.decode("utf-8").split("\n"):
            if not line:
                continue
            for port in line.split(","):
                if port:
                    binding = port.split("->")[0].strip()
                    port = binding.replace("/tcp", "").split(":")[-1]
                    if "-" in port:
                        ports.extend(
                            range(int(port.split("-")[0]), int(port.split("-")[1]) + 1)
                        )
                    else:
                        ports.append(int(port))
    except Exception as e:
        print(e)
    return list(sorted(set(ports)))


def confirm(question: str) -> bool:
    """
    Prompts the user with a question and returns True if the user confirms
    """
    answer = input(f"{question} [y/n]: ")
    return answer.strip().lower() in ("y", "yes")
