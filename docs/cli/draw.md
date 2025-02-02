# Draw commands

**Draw commands** are the *bread and butter* of `ttt`. Here's all the wonderful things you can do with this command group:

- Draw [images](#ttt-draw-image) and built-in [Icons](#ttt-draw-icon):

{{ example(
    'Image(get_icon("31")).blit()', command="ttt draw icon -d 39",
    indent=4
) }}

- Cut off sprites from sprite [atlases](#ttt-draw-atlas):

{{ example(
    'Image(get_icon("759")).blit()',
    command="ttt draw atlas icons.png -w 16 -h 16 -ox 8 -oy 8 -gx 8 -gy 8 -i 318",
    indent=4
) }}

- Draw [banners](#ttt-draw-banner) of repeating patterns:

{{ example(
    'Banner("flo1").blit(available_width=154)',
    command="ttt draw banner -d flo1",
    indent=4
) }}

---

::: mkdocs-click
    :module: ttt.cli.draw
    :command: draw
    :prog_name: ttt draw
    :style: table
