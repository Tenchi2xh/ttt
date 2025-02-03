# Frame

Surround some text with a nice **frame** and maybe an icon or two:

{{ example(
    'Frame(
        index="87",
        target=Row([
            Image(get_icon("34")),
            Text("I swear, officer,\\nI\'ve been framed!", font=find_font("m3x6")),
        ], gap=2),
    ).blit()',
    command="ttt frame -P -d 87 -f m3x6 -L 34 $'I swear, officer,\\nI\\'ve been framed!'"
) }}

You can also print piped outputs, and keep the text as-is:

{{ example(
    'Frame(
        index="38",
        target=RawBit("""github.com/AlDanial/cloc v 2.02
------------------------------------------------------------------------
Language              files          blank        comment           code
------------------------------------------------------------------------
Python                   33            454            192           1450
Text                     13            136              0            524
Cython                    1             30              3             75
------------------------------------------------------------------------
SUM:                     47            620            195           2049
------------------------------------------------------------------------"""),
    ).blit()',
    command="cloc src --hide-rate | ttt frame -V -d 76"
) }}

---

::: mkdocs-click
    :module: ttt.cli.frame
    :command: frame
    :prog_name: ttt frame
    :style: table
    :depth: 1
