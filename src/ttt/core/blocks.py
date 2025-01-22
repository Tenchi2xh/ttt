import numpy as np
from PIL import Image

"""
https://en.wikipedia.org/wiki/Symbols_for_Legacy_Computing_Supplement
U+1CD0x 𜴀 𜴁 𜴂 𜴃 𜴄 𜴅 𜴆 𜴇 𜴈 𜴉 𜴊 𜴋 𜴌 𜴍 𜴎 𜴏
U+1CD1x 𜴐 𜴑 𜴒 𜴓 𜴔 𜴕 𜴖 𜴗 𜴘 𜴙 𜴚 𜴛 𜴜 𜴝 𜴞 𜴟
U+1CD2x 𜴠 𜴡 𜴢 𜴣 𜴤 𜴥 𜴦 𜴧 𜴨 𜴩 𜴪 𜴫 𜴬 𜴭 𜴮 𜴯
U+1CD3x 𜴰 𜴱 𜴲 𜴳 𜴴 𜴵 𜴶 𜴷 𜴸 𜴹 𜴺 𜴻 𜴼 𜴽 𜴾 𜴿
U+1CD4x 𜵀 𜵁 𜵂 𜵃 𜵄 𜵅 𜵆 𜵇 𜵈 𜵉 𜵊 𜵋 𜵌 𜵍 𜵎 𜵏
U+1CD5x 𜵐 𜵑 𜵒 𜵓 𜵔 𜵕 𜵖 𜵗 𜵘 𜵙 𜵚 𜵛 𜵜 𜵝 𜵞 𜵟
U+1CD6x 𜵠 𜵡 𜵢 𜵣 𜵤 𜵥 𜵦 𜵧 𜵨 𜵩 𜵪 𜵫 𜵬 𜵭 𜵮 𜵯
U+1CD7x 𜵰 𜵱 𜵲 𜵳 𜵴 𜵵 𜵶 𜵷 𜵸 𜵹 𜵺 𜵻 𜵼 𜵽 𜵾 𜵿
U+1CD8x 𜶀 𜶁 𜶂 𜶃 𜶄 𜶅 𜶆 𜶇 𜶈 𜶉 𜶊 𜶋 𜶌 𜶍 𜶎 𜶏
U+1CD9x 𜶐 𜶑 𜶒 𜶓 𜶔 𜶕 𜶖 𜶗 𜶘 𜶙 𜶚 𜶛 𜶜 𜶝 𜶞 𜶟
U+1CDAx 𜶠 𜶡 𜶢 𜶣 𜶤 𜶥 𜶦 𜶧 𜶨 𜶩 𜶪 𜶫 𜶬 𜶭 𜶮 𜶯
U+1CDBx 𜶰 𜶱 𜶲 𜶳 𜶴 𜶵 𜶶 𜶷 𜶸 𜶹 𜶺 𜶻 𜶼 𜶽 𜶾 𜶿
U+1CDCx 𜷀 𜷁 𜷂 𜷃 𜷄 𜷅 𜷆 𜷇 𜷈 𜷉 𜷊 𜷋 𜷌 𜷍 𜷎 𜷏
U+1CDDx 𜷐 𜷑 𜷒 𜷓 𜷔 𜷕 𜷖 𜷗 𜷘 𜷙 𜷚 𜷛 𜷜 𜷝 𜷞 𜷟
U+1CDEx 𜷠 𜷡 𜷢 𜷣 𜷤 𜷥
...
U+1CEAx 𜺠     𜺣         𜺨     𜺫

https://en.wikipedia.org/wiki/Symbols_for_Legacy_Computing
U+1FB8x     🮂     🮅
...
U+1FBEx             🯦 🯧

https://en.wikipedia.org/wiki/Block_Elements
U+258x  ▀   ▂   ▄   ▆   █   ▊   ▌
U+259x  ▐           ▖ ▗ ▘ ▙ ▚ ▛ ▜ ▝ ▞ ▟
"""


block_map = """
  𜺨 𜺫 🮂 𜴀 ▘ 𜴁 𜴂 𜴃 𜴄 ▝ 𜴅 𜴆 𜴇 𜴈 ▀
𜴉 𜴊 𜴋 𜴌 🯦 𜴍 𜴎 𜴏 𜴐 𜴑 𜴒 𜴓 𜴔 𜴕 𜴖 𜴗
𜴘 𜴙 𜴚 𜴛 𜴜 𜴝 𜴞 𜴟 🯧 𜴠 𜴡 𜴢 𜴣 𜴤 𜴥 𜴦
𜴧 𜴨 𜴩 𜴪 𜴫 𜴬 𜴭 𜴮 𜴯 𜴰 𜴱 𜴲 𜴳 𜴴 𜴵 🮅
𜺣 𜴶 𜴷 𜴸 𜴹 𜴺 𜴻 𜴼 𜴽 𜴾 𜴿 𜵀 𜵁 𜵂 𜵃 𜵄
▖ 𜵅 𜵆 𜵇 𜵈 ▌ 𜵉 𜵊 𜵋 𜵌 ▞ 𜵍 𜵎 𜵏 𜵐 ▛
𜵑 𜵒 𜵓 𜵔 𜵕 𜵖 𜵗 𜵘 𜵙 𜵚 𜵛 𜵜 𜵝 𜵞 𜵟 𜵠
𜵡 𜵢 𜵣 𜵤 𜵥 𜵦 𜵧 𜵨 𜵩 𜵪 𜵫 𜵬 𜵭 𜵮 𜵯 𜵰
𜺠 𜵱 𜵲 𜵳 𜵴 𜵵 𜵶 𜵷 𜵸 𜵹 𜵺 𜵻 𜵼 𜵽 𜵾 𜵿
𜶀 𜶁 𜶂 𜶃 𜶄 𜶅 𜶆 𜶇 𜶈 𜶉 𜶊 𜶋 𜶌 𜶍 𜶎 𜶏
▗ 𜶐 𜶑 𜶒 𜶓 ▚ 𜶔 𜶕 𜶖 𜶗 ▐ 𜶘 𜶙 𜶚 𜶛 ▜
𜶜 𜶝 𜶞 𜶟 𜶠 𜶡 𜶢 𜶣 𜶤 𜶥 𜶦 𜶧 𜶨 𜶩 𜶪 𜶫
▂ 𜶬 𜶭 𜶮 𜶯 𜶰 𜶱 𜶲 𜶳 𜶴 𜶵 𜶶 𜶷 𜶸 𜶹 𜶺
𜶻 𜶼 𜶽 𜶾 𜶿 𜷀 𜷁 𜷂 𜷃 𜷄 𜷅 𜷆 𜷇 𜷈 𜷉 𜷊
𜷋 𜷌 𜷍 𜷎 𜷏 𜷐 𜷑 𜷒 𜷓 𜷔 𜷕 𜷖 𜷗 𜷘 𜷙 𜷚
▄ 𜷛 𜷜 𜷝 𜷞 ▙ 𜷟 𜷠 𜷡 𜷢 ▟ 𜷣 ▆ 𜷤 𜷥 █
"""


int_to_block = block_map[1:-1:2]
int_to_block_inverse = int_to_block[::-1]


def to_block_pil(image: Image, x0: int, y0: int, width: int, height: int, invert=False):
    pixels = np.array(image).astype(np.uint8) * 255
    return to_block(pixels, x0, y0, width, height, invert)


def to_block(pixels: np.ndarray, x0: int, y0: int, width: int, height: int, invert=False):
    c = 0 if invert else 255

    lines = []
    for y in range(y0, y0 + height, 4):
        line = []
        for x in range(x0, x0 + width, 2):
            block = np.zeros((4, 2), dtype=pixels.dtype)
            block[:min(4, pixels.shape[0] - y), :min(2, pixels.shape[1] - x)] = pixels[y:y + 4, x:x + 2]

            block_bits = (block == c).astype(np.uint8).flatten()
            block_value = np.packbits(block_bits[::-1])[0]

            line.append(block_value)
        lines.append(line)
    return lines
