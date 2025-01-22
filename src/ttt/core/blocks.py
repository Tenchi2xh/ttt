import numpy as np

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


def to_block(pixels, x0: int, y0: int, width: int, height: int, invert=False):
    c = 0 if invert else 255

    for y in range(y0, y0 + height, 4):
        line = []
        for x in range(x0, x0 + width, 2):
            block_value = 0
            for i in range(8):
                pixel_x = x + (i % 2)
                pixel_y = y + (i // 2)
                if pixel_x < x0 + width and pixel_y < y0 + height:
                  block_value |= (pixels[pixel_x, pixel_y] == c) << i
            line.append(block_value)
        yield line


# TODO: Optimize
def to_block_numpy(pixels: np.ndarray, x0: int, y0: int, width: int, height: int, invert=False):
    c = 0 if invert else 255

    for y in range(y0, y0 + height, 4):
        line = []
        for x in range(x0, x0 + width, 2):
            block = pixels[y:y + 4, x:x + 2]
            block = np.pad(block, ((0, max(0, 4 - block.shape[0])), (0, max(0, 2 - block.shape[1]))), constant_values=0)

            block_bits = (block == c).astype(np.uint8).flatten()

            block_value = 0
            for i, bit in enumerate(block_bits):
                block_value |= bit << i

            line.append(block_value)
        yield line
