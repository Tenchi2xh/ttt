# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

Using my wonderful tool, you can make flowers!

{{ example('Banner("flo1").blit()') }}

And write text!

{{ example('Text(
    "Hello, world!",
    font=find_font("kiwisoda")
).blit()') }}

---

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

```python
@draw.command()
@design_option("31", "icon")
@inject_blitter
def icon(design, blit):
    """
    Draw a built-in icon.

    Icons by PiiiXL (https://piiixl.itch.io)
    """

    image = Image(get_icon(design))
    blit(image)
```
