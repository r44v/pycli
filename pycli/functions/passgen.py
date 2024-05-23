import click
import colorama
import string
import random
colorama.init(autoreset=True)


@click.command()
@click.option("--short", 'option', flag_value="short")
@click.option("--easy", 'option', flag_value="easy")
def passgen(option, size = 50, chars=string.ascii_letters + string.digits + string.punctuation):
    if option == "short":
        size = 16
    elif option == "easy":
        size = 12
        chars=string.ascii_letters + string.digits
    click.echo(''.join(random.choice(chars) for _ in range(size)))