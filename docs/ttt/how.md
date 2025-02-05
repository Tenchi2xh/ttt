# How does it work?

Explaining how the rendering of the pixels work is actually quite straightforward. The interesting bit though is the history of how we got there.

Feel free to skip directly to the [technical explanation](#encoding)

---

## History

I present to you:

*A (very) short history of block graphics rendering in text-based interfaces*.

### 2×2 block graphics

How do you draw something on the screen when you can only display text?

Many classic computers in the 80s solved this problem by including characters in their character set that could be used for fake graphics (called [semigraphics](https://en.wikipedia.org/wiki/Semigraphics)) instead of using an expensive (or non-existent) framebuffer.

For example, let's take the [ZX80](https://en.wikipedia.org/wiki/ZX80) (1980), which had perfectly square text characters. It included in its character set 7 characters representing small grids of 2×2 pixels. Combined with a space character and by being able to invert colors, it was possible to represent all 16 possible combinations (plus some extra shading):

<center>
<pre class="blocks-2x2 center">
  ▘ ▝ ▀ ▖ ▌ ▞ ▛ ▒ 🮏 🮎

█ ▟ ▙ ▄ ▜ ▐ ▚ ▗ 🮐 🮑 🮒
</pre>
<em>ZX80 semigraphics character set,<br>represented with [Iosevka](install.md#compatible-fonts) glyphs stretched to 2.5×</em>
</center>

And here's a rendering of [icon #768](art-credits.md#icons) from `ttt`'s built-in icons using the ZX80 character set:

<center>
<pre class="blocks-2x2 center">
▌█▛▛▀▀██
▌▛▀▀▀▀▀▜
▌▌▞▖▄▗▚▐
▌▌▝   ▘▐
▌█▀▀▀▀▀█
▌▌█████▐
</pre>
<em>Should this be the save icon?</em>
</center>

Many other computers of the time used similar 2×2 block graphics, for example the [Dragon 32/64](https://en.wikipedia.org/wiki/Dragon_32/64) (1982, 1983), the [Panasonic JR-200](https://en.wikipedia.org/wiki/Panasonic_JR-200) (1983), and the [Amstrad CPC](https://en.wikipedia.org/wiki/Amstrad_CPC) and of course the [Commodore PET](https://en.wikipedia.org/wiki/Commodore_PET)[^commodore].

[^commodore]: The Commodore PET included much more than just 2×2 characters: [PETSCII](https://en.wikipedia.org/wiki/PETSCII) also added shading characters, box-drawing characters, diagonal lines, horizontal lines at various heights, diagonally filled blocks, etc.<br><br>This made it possible to draw incredibly detailed art despite being only text-based. The PETSCII Art community is still going strong today, [check it out](https://tomseditor.com/gallery/browse?lang=en&platform=commodore&format=petscii&year=&author=&nsfw=0&sort=score)!

### 2×3 block graphics

Other computers had taller characters, much like what you are reading right now, where displaying 2×2 blocks would look distorted.

Since these taller characters have a ratio of 2:3, the obvious thing to do is to divide blocks into 2×3 pixels, resulting in the following 64-character set:

<center>
<pre class="blocks-2x3 center">
  🬀 🬁 🬂 🬃 🬄 🬅 🬆 🬇 🬈 🬉 🬊 🬋 🬌 🬍 🬎

🬏 🬐 🬑 🬒 🬓 ▌ 🬔 🬕 🬖 🬗 🬘 🬙 🬚 🬛 🬜 🬝

🬞 🬟 🬠 🬡 🬢 🬣 🬤 🬥 🬦 🬧 ▐ 🬨 🬩 🬪 🬫 🬬

🬭 🬮 🬯 🬰 🬱 🬲 🬳 🬴 🬵 🬶 🬷 🬸 🬹 🬺 🬻 █
</pre>
<em>Full set of 2×3 block graphics,<br>represented with [Iosevka](install.md#compatible-fonts) glyphs stretched to 1.667×</em>
</center>

This lets us draw, _with the same line height_, an **extra 50% pixels**! (Or, conversely, draw the same number of pixels with 33% less lines)

<center>
<pre class="blocks-2x3 center">
▌█🬴🬴🬰🬰██
▌▌🬖🬏🬭🬞🬢▐
▌🬲🬯🬭🬭🬭🬮🬷
▌🬕🬹🬹🬹🬹🬹🬨
</pre>
</center>

The cassette drawn here uses only 4 lines, whereas the one drawn earlier with 2×2 blocks used 6 lines.

Although this results in a higher resolution, it is not a chronological "evolution" from the previously mentioned computers, just another contemporary approach. Computers that used 2×3 block graphics include the [TRS-80](https://en.wikipedia.org/wiki/TRS-80) (1977) and the [BBC Micro](https://en.wikipedia.org/wiki/BBC_Micro).

If you're from Europe, this should remind you of [Teletext](https://en.wikipedia.org/wiki/Teletext), which used this exact character set to draw its graphics!

### 2×4 block graphics

How do we level up from there? That's right, a 256-character set of 2×4 blocks.

From my research, very few computers supported 2×4 block graphics, all from [Kaypro](https://en.wikipedia.org/wiki/Kaypro): the Kaypro Ⅱ, Kaypro Ⅳ and Kaypro 10[^kaypro].

[^kaypro]: [https://www.chrisfenton.com/exploring-kaypro-video-performance/](https://www.chrisfenton.com/exploring-kaypro-video-performance/)

This is understandable, since on an 8-bit computer, the maximum number of characters supported in any given character set would be 256.

Even though they stored only half of the 2×4 blocks to save space (the other half being producible by inverting the colors of the characters), this would fill ***half*** of their character space, leaving very little room for practical use!

Below is the complete 256-character set of 2×4 blocks:

<center>
<pre>
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
</pre>
<em>Now we're cooking[^sorted].</em>
</center>

[^sorted]: This table took a whole day to write by hand (it's used in `blocks.py`).<br><br>Because Unicode is very economical and refuses to issue duplicate characters, when they introduced the 2×4 characters, the new Unicode block left out a lot of characters that were already represented in other blocks, such as half blocks, quarter blocks, etc.<br><br>However, the address space itself doesn't leave any gap where those characters are missing, so a lot of manual work was needed to write all these characters in the correct binary order, piecing it up from 3 different Unicode blocks.

And again, here is our little cassette tape, this time only using 3 lines of text, giving us much more resolution at the cost of character set space. Compared to using 2×2 blocks, that's *four times* the resolution, and we only need half the lines of text to display the same image.

<center>
<div class="example">
<pre class="blocks-2x4">
▌𜵰𜴮𜴮𜴪𜴪🮅𜶫
▌▌𜴞𜴀𜴆𜴃𜴑▐
▌▛𜷝𜷝𜷝𜷝𜷝▜
</pre>
</div>
<em>Only 3 lines of text!</em>
</center>

And here we can see all three systems side by side:

<center>
<div class="side-by-side">
<pre class="blocks-2x2 center">
▌█▛▛▀▀██
▌▛▀▀▀▀▀▜
▌▌▞▖▄▗▚▐
▌▌▝   ▘▐
▌█▀▀▀▀▀█
▌▌█████▐
</pre>
<pre class="blocks-2x3 center">
▌█🬴🬴🬰🬰██
▌▌🬖🬏🬭🬞🬢▐
▌🬲🬯🬭🬭🬭🬮🬷
▌🬕🬹🬹🬹🬹🬹🬨
</pre>
<pre class="blocks-2x4">
▌𜵰𜴮𜴮𜴪𜴪🮅𜶫
▌▌𜴞𜴀𜴆𜴃𜴑▐
▌▛𜷝𜷝𜷝𜷝𜷝▜
</pre>
</div>
</center>

You'll notice that the last one looks slightly vertically compressed, and that's because the native aspect ratio of [Iosevka](install.md#compatible-fonts) is actually 1:2.5, slightly more tall than the optimal 1:2 needed to render 2×4 blocks.

### Modern day

But that's all for old computers, how do we draw stuff in our current terminal emulators, without bitmap character sets?

You'll notice that so far, we've managed to show all those ancient characters in a modern browser. All the examples above are real text (go ahead and try to select them), and that's all thanks to Unicode.

Almost as far back as Unicode goes (version 1.1.0), and before that in various other encodings[^cp437], it was possible to draw "pixels" in a terminal using the *UPPER HALF BLOCK* and *LOWER HALF BLOCK* characters: ▀ and ▄.

With those, we could draw very big pixels (that's twice as big as the very first example we had with primitive 2×2 blocks!), but that's all we could draw for a long while.

Then, revision after revision, the Unicode consortium blessed us with more and more characters:

Type            | * | Year | Unicode block                                                                                                    | Aspect ratio | Resolution
---------------:|---|:----:|------------------------------------------------------------------------------------------------------------------|:------------:|-----------------------
1×2&nbsp;blocks | ▀ | 1991 | [Block Elements](https://en.wikipedia.org/wiki/Block_Elements) (Unicode 1.0)                                     | 1:2          | 2&nbsp;ppc
2×2&nbsp;blocks | ▞ | 2002 | [Block Elements](https://en.wikipedia.org/wiki/Block_Elements) (Unicode 3.2)                                     | 1:1          | 4&nbsp;ppc
2×3&nbsp;blocks | 🬤 | 2020 | [Symbols for Legacy Computing](https://en.wikipedia.org/wiki/Symbols_for_Legacy_Computing)                       | 2:3          | 6&nbsp;ppc
Braille         | ⡪ | 1999 | [Braille Patterns](https://en.wikipedia.org/wiki/Braille_Patterns)                                               | 1:2          | 8&nbsp;ppc<sup>*</sup>
2×4&nbsp;blocks | 𜵗 | 2024 | [Symbols for Legacy Computing Supplement](https://en.wikipedia.org/wiki/Symbols_for_Legacy_Computing_Supplement) | 1:2          | 8&nbsp;ppc

[^cp437]: For example, the famous [Code Page 437](https://en.wikipedia.org/wiki/Code_page_437)

For a long time, the best resolution we could achieve was by using *braille dots*, since Unicode was nice enough to add all possible dot combination (even if they were not actually used in any braille script).

Drawing using small dots was never more than just a gimmick however. Since the dots are so small, and the gap between the lines was quite big, it was hard to be able to visually parse any generated image using this character set:

<center>
<div class="example">
<pre class="blocks-2x4">
⡇⡿⠯⠯⠭⠭⠿⢿  ▌𜵰𜴮𜴮𜴪𜴪🮅𜶫
⡇⡇⠪⠂⠒⠐⠕⢸  ▌▌𜴞𜴀𜴆𜴃𜴑▐
⡇⡟⣭⣭⣭⣭⣭⢻  ▌▛𜷝𜷝𜷝𜷝𜷝▜
</pre>
</div>
<em>Braille rendering vs. native 2×4 blocks</em>
</center>

But then suddenly, out of nowhere, came the "Symbols for Legacy Computing Supplement" block, officially adding native 2×4 block characters.

It's kind of a miracle that these 2×4 block graphics were added to Unicode at all. In the [initial proposal for adding more legacy computer graphic characters](https://www.unicode.org/L2/L2021/21235-terminals-supplement.pdf), the inclusion of the "block octant graphics" from the Kaypro computers was evaluated to be of only "medium" importance, ranking 5 out of 7 for priority.

Thanks to that, we can now have lots of fun in our modern terminals!

## Encoding

TODO explain:

- Encoding an image into a number
    - LUT
