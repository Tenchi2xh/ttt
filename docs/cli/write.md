# Write

Using the **write command**, you can transform regular text into beautiful, giant letters in the terminal:

{{ example(
    'Text(
        "Hello, world!",
        font=find_font("kiwisoda")
    ).blit()',
    command="ttt write -f kiwisoda 'Hello, world!'"
) }}

And since text commands accept inputs from pipes, the following _POSIX madness_ is not only possible but also very awesome:

```bash
$ ls -al | head -3 | ttt write -f m3x6
```

<pre>
𜶦𜴉𜵋𜵈𜶦𜴉𜵼▖▌   𜶛 𜵳𜴍𜵳🯦𜵦𜴺
▝ 𜴇𜺨▝ 𜴇▘𜴄   𜴈𜴀▝ 𜴇𜴀▘▘
𜵋▌𜵋𜴀𜵈▖𜵈𜶄🯦𜵋𜴀▂𜺣𜶄🯦𜵋𜴀▂𜺣𜶄🯦 𜺫𜵚𜴃▌  𜶦𜴉𜷃𜵈𜵎▖𜵋𜴀𜵏▖𜵅  𜶖𜶃𜺫𜵜𜺫𜵚  𜵧𜺨𜷃𜵈𜵏▖   𜺫𜵚  𜵳🯦𜵳🯦𜴉𜴮𜴶𜴮𜴶
𜴇▘▘ 𜴄𜴄𜺨▘▘▘   ▘▘▘   ▘▘ ▝𜴆𜴃𜴇  ▝ 𜴄𜴀▘▘𜴇𜴀▘▘▘  𜺫𜴈 ▘▝𜴆  ▘ 𜴄𜴀𜴇▘   ▝𜴆  𜴇𜴀𜴇𜴀𜴀𜴆𜺨𜴆𜺨 𜴃
𜵋▌𜵋𜴀𜵈▖𜵈𜶄🯦𜵋𜴀▂𜺣𜶄🯦𜵋𜴀▂𜺣𜶄🯦 ▝𜶦𜶖𜶃  𜶦𜴉𜷃𜵈𜵎▖𜵋𜴀𜵏▖𜵅 𜴃▌ 𜴡𜶃▐𜶊  🮂▌𜵼▖𜵎▖ 𜺫𜵚𜶖𜶘  𜶛 𜴪𜴹𜴉𜴮𜴶𜴮𜴶
𜴇▘▘ 𜴄𜴄𜺨▘▘▘   ▘▘▘   ▘▘  ▝𜺫𜴈  ▝ 𜴄𜴀▘▘𜴇𜴀▘▘▘ 𜴃𜴇𜴃𜴃𜴁▝▝  𜴆𜺨𜴇▘▘▘ ▝𜴆▝𜴁  𜴈𜴀𜴆𜺨𜴀𜴆𜺨𜴆𜺨 𜴃𜴃
</pre>

Make sure to check out all the different fonts using [`ttt list fonts`](list.md)!

---

::: mkdocs-click
    :module: ttt.cli.write
    :command: write
    :prog_name: ttt write
    :style: table
    :depth: 1