# Installation

Installing `ttt` is straight-foward:

```bash
pipx install ttt
```

Optionally:

- If you want video, you will need to install [`ffmpeg`](#fn:ffmpeg)[^ffmpeg] on your system.
- And if you want some audio with your video, you'll need [`portaudio`](#fn:portaudio)[^portaudio], and install `pipx install ttt[audio]` instead of the command above.

[^ffmpeg]: On macOS: `brew install ffmpeg`.<br>On Ubuntu: `apt-get install ffmpeg`.<br>On Windows: ¯\\\_(ツ)\_/¯
[^portaudio]: On macOS: `brew install portaudio`.<br>On Ubuntu: `apt-get install portaudio19-dev python3-all-dev`.<br>On Windows, the binaries are bundled.

You should now be able to use the `ttt` command, but probably won't be able to see any output!

To fix that, you'll need to install a **compatible font**. Then, to correctly render the output, you'll need to **set up your terminal emulator**.

---

## Compatible fonts

Any font that's monospace and implements the [Symbols for Legacy Computing Supplement](https://en.wikipedia.org/wiki/Symbols_for_Legacy_Computing_Supplement) Unicode block should be compatible.

However, as of writing, only *two fonts* (!) implement this Unicode block:

- [Iosevka](https://github.com/be5invis/Iosevka): huge unicode coverage, *extremely* customizable, ligatures support, my favorite monospace font!

{{ example(
    'Row(
        [
            RawBit(" "),
            Image(get_icon("175")),
            RawBit("\\n"
                "Check out my custom Iosevka variant, <a href=\\"https://github.com/Tenchi2xh/IosevkaKotan/releases\\">Iosevka Kotan</a>.\\n"
                "(It\'s the font you\'re reading right now!)\\n"
                ""
            )
        ],
        gap=2,
    ).blit()',
    only_example=True,
) }}

- [Cascadia Code](https://github.com/microsoft/cascadia-code): made by Microsoft, bundled with Windows Terminal, seems pretty decent.

{{ example(
    'Row(
        [
            Image(get_icon("134")),
            RawBit("<b>Note</b>: If you don\'t like either those fonts, that\'s fine!\\n"
                "You don\'t need to actually use them as your terminal font, but\\n"
                "you can still install one of them so that your OS can use it as\\n"
                "a fallback font, only for the required missing Unicode blocks."
            )
        ],
        gap=4,
    ).blit()',
    only_example=True,
) }}

---

## Setting up your terminal emulator

To correctly display `ttt`'s outputs to the screen:

- Make sure the **character width** and **line height** are set to defaults (in iTerm, the `v|i` and `n|n` settings should be set to 100).

{{ example(
    'Row(
        [
            RawBit(" "),
            Image(get_icon("134")),
            RawBit("<b>Note</b>: If using a font other than the ones <a href=\\"#compatible-fonts\\">listed above</a>,\\n"
                "try to adapt those two settings to match the aspect ratio of\\n"
                "the fallback font you installed. For Iosevka, the native ratio\\n"
                "of its block characters is exactly 16:40, and Cascadia 18:40."
            )
        ],
        gap=4,
    ).blit()',
    only_example=True,
) }}

- If using *Iosevka*, use the "Iosevka Term" variant, which is narrower.
