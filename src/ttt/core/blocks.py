import numpy as np
from PIL import Image

from .convert import to_blocks


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


def to_blocks_pil(image: Image, x0: int, y0: int, width: int, height: int, invert=False):
    pixels = np.array(image).astype(np.uint8) * 255
    return to_blocks(pixels, x0, y0, width, height, invert)
