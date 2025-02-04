from dataclasses import dataclass
from typing import Literal

from .fonts import all_fonts


licenses = {
    "sil": "SIL Open Font License",
    "ccby40": "CC BY 4.0",
    "ccbynd40": "CC BY-ND 4.0",
    "ccbysa30": "CC BY-SA 3.0",
    "cc0": "CC0 1.0",
}

license_urls = {
    "sil": "https://openfontlicense.org/open-font-license-official-text/",
    "ccby40": "https://creativecommons.org/licenses/by/4.0/",
    "ccbynd40": "https://creativecommons.org/licenses/by-nd/4.0/",
    "ccbysa30": "https://creativecommons.org/licenses/by-sa/3.0/",
    "cc0": "https://creativecommons.org/publicdomain/zero/1.0/",
}

type License = Literal["font", "icon", "pattern", "frame"]


@dataclass
class Credit:
    category: License
    name: str
    author: str
    url: str
    license: str
    asset_ids: list[str] | None = None

    @property
    def license_name(self):
        return licenses[self.license]

    @property
    def license_url(self):
        return license_urls[self.license]


credits: list[Credit] = []

for font in all_fonts:
    existing = next(
        (c for c in credits if c.name == font.name and c.author == font.author), None
    )

    if existing and existing.asset_ids:
        existing.asset_ids.append(font.id)

    else:
        credits.append(
            Credit(
                category="font",
                name=font.name,
                author=font.author,
                url=font.url,
                license=font.license,
                asset_ids=[font.id],
            )
        )

credits.extend(
    [
        Credit(
            category="frame",
            name="Frames 1-Bit",
            author="PiiiXL",
            url="https://piiixl.itch.io/frames-1-bit",
            license="ccby40",
            asset_ids=["52", "33", "73"],
        ),
        Credit(
            category="icon",
            name="1-Bit Icons Part-I",
            author="PiiiXL",
            url="https://piiixl.itch.io/1-bit-16px-icons-part-1",
            license="ccbynd40",
            asset_ids=["14", "31", "37", "193", "381", "4", "134", "164"],
        ),
        Credit(
            category="icon",
            name="1-Bit Icons Part-II",
            author="PiiiXL",
            url="https://piiixl.itch.io/1-bit-icons-part-2",
            license="ccbynd40",
            asset_ids=["466", "467", "510", "525", "685", "699", "766", "767"],
        ),
        Credit(
            category="pattern",
            name="100x2 seamless 1bit patterns (pack1)",
            author="Lettercore",
            url="https://lettercore.itch.io/1bitpatterns-pack1",
            license="ccby40",
            asset_ids=["knot1", "crystalnet0", "cards0"],
        ),
        Credit(
            category="pattern",
            name="100x2 seamless 1bit patterns (pack2)",
            author="Lettercore",
            url="https://lettercore.itch.io/1bitpatterns-pack2",
            license="ccby40",
            asset_ids=["flo1", "bubbles1", "ponywave0"],
        ),
        Credit(
            category="pattern",
            name="100x2 seamless 1bit patterns (pack3)",
            author="Lettercore",
            url="https://lettercore.itch.io/1bitpatterns-pack3",
            license="ccby40",
            asset_ids=["beadwork0", "ornam4", "classic0"],
        ),
    ]
)
