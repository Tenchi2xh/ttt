from collections import defaultdict
import json
from pathlib import Path
from fontTools.ttLib import TTFont, TTCollection

unicode_ranges = {
    "Basic Latin":            (0x0020, 0x007F, "Latin"),
    "Latin Extended-A":       (0x0100, 0x017F, "Latin+"),
    "Greek and Coptic":       (0x0370, 0x03FF, "Greek"),
    "Cyrillic":               (0x0400, 0x04FF, "Cyrillic"),
    "Hebrew":                 (0x0590, 0x05FF, "Hebrew"),
    "Arabic":                 (0x0600, 0x06FF, "Arabic"),
    "Runic":                  (0x16A0, 0x16FF, "Runic"),
    "Hiragana":               (0x3040, 0x309F, "Hiragana"),
    "Katakana":               (0x30A0, 0x30FF, "Katakana"),
    # "CJK Unified Ideographs": (0x4E00, 0x9FFF, "CJK Ideographs"),
    "Hangul Syllables":       (0xAC00, 0xD7AF, "Korean"),
}

CJK_simplified  = "爱门国鱼车马云叶语"
CJK_traditional = "愛門國魚車馬雲葉語"

supported_threshold = 10


false_reports = {
    "vhsgothic": ["Hiragana", "Katakana", "Cyrillic"],
}


def determine_character_sets(font_path: Path):
    if font_path.suffix.lower() == ".ttc":
        collection = TTCollection(font_path)
        supported_code_points = set()
        for font in collection:
            cmap = font["cmap"]
            unicode_maps = cmap.getBestCmap()
            supported_code_points |= set(unicode_maps.keys())
    else:
        font = TTFont(font_path)
        cmap = font["cmap"]
        unicode_maps = cmap.getBestCmap()
        supported_code_points = set(unicode_maps.keys())

    supported_sets = defaultdict(int)
    for _, (start, end, simple_name) in unicode_ranges.items():
        charset_range = set(range(start, end + 1))
        overlap = supported_code_points & charset_range
        if overlap and simple_name not in false_reports.get(font_path.stem, []):
            supported_sets[simple_name] += len(overlap)

    supported = [k for k, v in supported_sets.items() if v > supported_threshold]

    if all(ord(c) in supported_code_points for c in CJK_simplified):
        supported.append("CJK Simplified")

    if all(ord(c) in supported_code_points for c in CJK_traditional):
        supported.append("CJK Traditional")

    return supported


fonts_path = Path("src/ttt/resources/fonts")
for font_path in fonts_path.glob("*.tt[c,f]"):
    supported_sets = determine_character_sets(font_path)
    with open(font_path.with_suffix(".json"), "r+") as f:
        data = json.load(f)
        data["charsets"] = supported_sets
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
