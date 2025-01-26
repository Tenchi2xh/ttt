# `ttt`

TODO: Show some screenshots and gifs

## Usage

- Draw a sprite from a sprite atlas:

  ```bash
  ttt draw atlas resources/1bit_icons_i_by_PiiiXL.png -w 16 -h 16 -ox 8 -oy 8 -gx 8 -gy 8 -i 31
  ```

- List supported fonts and languages, with a hard outline effect:

  ```bash
  ttt write -l -o hard
  ```

- WATCH F-ING BAD APPLE AT A SMOOTH FRAMERATE WITH AUDIO:

  ```bash
  ttt watch "https://dn720401.ca.archive.org/0/items/TouhouBadApple/Touhou%20-%20Bad%20Apple.mp4" -a -m
  ```

> [!NOTE]
> Did you know? The video player is SO FAST it can reach up to _**2000**_ FPS!
> You can disable the frame rate limit with the `-F` option.

## Requirements

- A terminal emulator set up to ensure characters have a 1:2 aspect ratio, with no line spacing

- A monospace font that implements the [Symbols for Legacy Computing Supplement](https://en.wikipedia.org/wiki/Symbols_for_Legacy_Computing_Supplement) Unicode block:
  - [Iosevka](https://github.com/be5invis/Iosevka) (recommended, customizable, my favorite font!)

    Check out my custom variant, [Iosevka Kotan](https://github.com/Tenchi2xh/IosevkaKotan/releases)
  - [Cascadia Code](https://github.com/microsoft/cascadia-code)

> [!TIP]
> If you don't like those fonts, that's fine! You don't need to use them as your terminal font, but you can still install one of them so that your OS will use it as a fallback font only for the required Unicode block.

- Optionally, for video support: `ffmpeg`:

  ```bash
  brew install ffmpeg
  ```

- On macOS, `pyaudio` needs an extra dependency before the package can be installed (other OSes are fine):

  ```bash
  brew install portaudio
  ```

## Installation

TODO

## Development

- Before running locally, run:

```bash
poetry install
```

- Adding new fonts:

  Add `fontname` to the list of font names in `src/ttt/resources/fonts/fonts.py`. The font name should be in all lowercase and no punctuations. If the font is a variant, then `fontname-variant`.

  Add the following files:
    1. `src/ttt/resources/fonts/fontname.ttf`: the main font file (`.ttc` also supported)
    1. `src/ttt/resources/fonts/fontname.txt`: font readme or license
    1. `src/ttt/resources/fonts/fontname.json`: font config (see other fonts)

  Finally, to update the font config with its supported languages, run:

  ```bash
  poetry run python tools/font_languages.py
  ```
