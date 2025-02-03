# Watch

Now, please hold on to your seat tightly.

...

Ok, all good?

Yes, it's true. `ttt` can play videos. In monochrome of course, but also in colors. Kind of. At thousands of frames per second!

I can't show it here, but here are two classics to enjoy:

- Monochrome:

    <div class="example">
    ```bash
    curl -L -O bad_apple.mp4 "https://archive.org/download/TouhouBadApple/Touhou%20-%20Bad%20Apple.mp4"
    ttt watch -m -a bad_apple.mp4
    ```
    </div>

- Color:

    <div class="example">
    ```bash
    curl -L -O rick.mp4 "https://archive.org/download/rick-astley-never-gonna-give-you-up_202302/Rick_Astley_Never_Gonna_Give_You_Up.mp4"
    ttt watch -m -a -c rick.mp4
    ```
    </div>

{{ example(
    'Row([
        Image(get_icon("lightbulb")),
        RawBit("Tip!\\n\\n"
            "Since the watch command\'s backend is ffmpeg, it is possible to call the\\n"
            "watch command directly with a URL, but the initial load is quite slow."
        )]).blit()',
    only_example=True,
) }}

---

::: mkdocs-click
    :module: ttt.cli.watch
    :command: watch
    :prog_name: ttt watch
    :style: table
    :depth: 1
