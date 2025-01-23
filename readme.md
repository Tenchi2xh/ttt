# ttt

## Usage

- Sprite from a sprite atlas:

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

> [!TIP]
> Did you know? The video player is SO FAST it can reach up to _**2000**_ FPS!
> You can disable the frame rate limit with the `-F` option.

## Requirements

- `ffmpeg`

### macOS

On macOS, `pyaudio` needs an extra dependency before the package can be installed (other OSes are fine):

```bash
brew install portaudio
```

## Development

Before running locally, run:

```bash
poetry install
```

To make VSCode happy, run:

```bash
poetry run python tools/vs_code.py
```
