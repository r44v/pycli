import click
from .helpers import load_env, read_env, print_with_glow


@click.group(invoke_without_command=False)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        ...


@cli.command()
def diff():
    """Open VSCode diff tool"""
    from pycli.functions.codediff import codediff

    codediff()


@cli.command()
def guid():
    """Generate a new GUID"""
    import uuid

    print(str(uuid.uuid4()))


@cli.command()
@click.option("-c", "--compact", "compact", is_flag=True)
@click.option("-l", "--local", "local", is_flag=True)
def now(compact, local):
    """Generate current utc time in ISO format"""
    from datetime import datetime, timezone

    FORMAT = "%Y%m%dT%H%M%S"
    now = datetime.now() if local else datetime.now(tz=timezone.utc)
    if compact:
        print(now.strftime(FORMAT + ("%z" if local else "Z")))
    else:
        print(now.isoformat())


@cli.command()
@click.argument("publishprofile", type=click.Path(exists=True))
def ftp(publishprofile):
    """Open publish profile in FileZilla"""
    from pycli.functions.azure.ftp import open_publish_profile_in_filezilla

    open_publish_profile_in_filezilla(publishprofile)


from pycli.functions.passgen import passgen

cli.add_command(passgen)


@cli.command()
@click.argument("host")
@click.argument("port", type=click.INT)
def portup(host, port):
    """Check if a port is up"""
    from pycli.functions.portup import portup as portupcmd

    try:
        import colorama

        colorama.init()
        GREEN = colorama.Fore.GREEN
        RED = colorama.Fore.RED
        CYAN = colorama.Fore.CYAN
    except ImportError:
        GREEN = "\033[32;1;40m"
        RED = "\033[31;1;40m"
        CYAN = "\033[36;1;40m"

    print(CYAN + "Testing")
    print("  " + host + ":" + str(port))

    if portupcmd(host, port):
        print(GREEN + "Port UP")
    else:
        print(RED + "Port DOWN")


@cli.command()
def ip():
    """Returns external ipv4 IP address"""
    from pycli.functions.getip import get_external_ip

    ip = get_external_ip()
    print(ip)


@cli.command()
@click.argument("question", required=False, nargs=-1)
def ask(question: tuple[str]):
    """Converse with chatGPT"""
    load_env()
    from pycli.functions.chat import ask

    if not question:
        question = input("Ask a question: ")
    else:
        question = " ".join(question)

    history, answer = ask(question)
    print_with_glow(answer)

    while 1:
        question: str = input(">: ")
        exit_if = ("exit", "quit", "bye", "goodbye", "q")
        if any(question.strip().lower() == e for e in exit_if):
            print("Bye")
            break
        history, answer = ask(question, history)
        print_with_glow(answer)


@cli.command()
def image():
    """Generate an image with DALL-E"""
    load_env()
    from pycli.functions.image import create

    prompt = input("Prompt: ")
    create(prompt)


@cli.command()
@click.argument("query", required=False)
def search(query: str):
    """Search via duckduckgo"""
    if not query:
        query = input("search query: ")

    import webbrowser
    import urllib.parse

    webbrowser.open("https://duckduckgo.com/?q=" + urllib.parse.quote(query))


@cli.command()
@click.argument("query", required=False)
def google(query: str):
    """Seach via google"""
    if not query:
        query = input("search query: ")

    import webbrowser
    import urllib.parse

    webbrowser.open("https://www.google.com/search?q=" + urllib.parse.quote(query))


@cli.command()
def temp():
    """Start temp project"""
    from pycli.functions.temp import make_temp_project

    make_temp_project()


# region docker


@click.group(invoke_without_command=False)
def docker(): ...


@docker.command("ps")
def docker_ps():
    from pycli.functions.docker import docker_ps

    docker_ps()


@docker.command("exec")
@click.argument("container")
def docker_ps(container: str):
    from pycli.functions.docker import docker_exec

    docker_exec(container)


@docker.command("stop")
def docker_stop():
    from pycli.functions.docker import docker_stop

    docker_stop()


cli.add_command(docker)

# endregion


from pycli.functions.timer import timer

cli.add_command(timer)


from pycli.functions.dotnet import dotnet

cli.add_command(dotnet)


def load_hidden_functions():
    """
    Dynamically loads modules defined using the following environment variables
    PYCLI_FUNCTION_HIDDEN=pycli_hidden.hidden:cli

    where the name will be hidden (lowercased HIDDEN after the prefix)
    pycli_hidden will be a module in the root of this project
    in this folder a file called hidden.py needs to have click group called cli

    > import click
    >
    > @click.group(invoke_without_command=False)
    > def cli():
    >    ...

    """
    import importlib
    import pathlib
    import sys

    prefix = "PYCLI_FUNCTION_"
    hidden_imports = {k: v for k, v in read_env().items() if k.startswith(prefix)}

    if not hidden_imports:
        return

    ROOT = pathlib.Path(__file__).parent.parent
    sys.path.insert(0, ROOT.as_posix())

    for key, value in hidden_imports.items():
        if key.startswith(prefix):
            function_name = key[15:].lower()
            module_name, import_name = str.split(value, sep=":", maxsplit=1)
            module = importlib.import_module(module_name)
            func = getattr(module, import_name)
            cli.add_command(func, function_name)
    
    sys.path.pop(0)

load_hidden_functions()
