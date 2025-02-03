# List commands

Find the perfect icon or font using the **list commands**.

{{ example(
    'Row([
        Image(get_icon("lightbulb")),
        RawBit("Tip!\\n\\n"
            "You can provide a TEXT argument to the \'list fonts\' command\\n"
            "to preview all the fonts with your own text. Handy!"
        )]).blit()',
    only_example=True,
) }}

---

::: mkdocs-click
    :module: ttt.cli.list
    :command: list
    :prog_name: ttt list
    :style: table
    :depth: 1
