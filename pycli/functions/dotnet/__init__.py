import click


@click.group(invoke_without_command=False)
def dotnet():
    ...

@dotnet.command()
def clean():
    from .clean import run
    run()
