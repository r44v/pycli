import subprocess

def docker_ps():
    subprocess.call(
        'docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}"',
        shell=True,
    )


def docker_stop():
    containers = (
        subprocess.check_output('docker ps --format "{{.ID}}"', shell=True)
        .decode("utf-8")
        .splitlines()
    )

    if containers:
        subprocess.call(f"docker stop {str.join(" ", containers)}", shell=True)
    print("Stopped all containers:")


def docker_exec(container: str):
    cmd = f"docker exec -it {container} bash"
    subprocess.call(cmd, shell=True)