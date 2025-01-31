import click


context_settings = {
    "help_option_names": ["-h", "--help"],
    "max_content_width": 100,
}


@click.group(context_settings=context_settings)
def ttt():
    pass
