from collections import defaultdict
import json
from pathlib import Path
from fontTools.ttLib import TTFont

unicode_ranges = {
    "Basic Latin":            (0x0020, 0x007F, "Latin"),
    "Latin Extended-A":       (0x0100, 0x017F, "Latin+"),
    "Latin Extended-B":       (0x0180, 0x024F, "Latin+"),
    "Greek and Coptic":       (0x0370, 0x03FF, "Greek"),
    "Cyrillic":               (0x0400, 0x04FF, "Cyrillic"),
    "Cyrillic Supplementary": (0x0500, 0x052F, "Cyrillic+"),
    "Armenian":               (0x0530, 0x058F, "Armenian"),
    "Hebrew":                 (0x0590, 0x05FF, "Hebrew"),
    "Arabic":                 (0x0600, 0x06FF, "Arabic"),
    "Syriac":                 (0x0700, 0x074F, "Syriac"),
    "Thaana":                 (0x0780, 0x07BF, "Thaana"),
    "Devanagari":             (0x0900, 0x097F, "Devanagari"),
    "Bengali":                (0x0980, 0x09FF, "Bengali"),
    "Gurmukhi":               (0x0A00, 0x0A7F, "Gurmukhi"),
    "Gujarati":               (0x0A80, 0x0AFF, "Gujarati"),
    "Oriya":                  (0x0B00, 0x0B7F, "Oriya"),
    "Tamil":                  (0x0B80, 0x0BFF, "Tamil"),
    "Telugu":                 (0x0C00, 0x0C7F, "Telugu"),
    "Kannada":                (0x0C80, 0x0CFF, "Kannada"),
    "Malayalam":              (0x0D00, 0x0D7F, "Malayalam"),
    "Sinhala":                (0x0D80, 0x0DFF, "Sinhala"),
    "Thai":                   (0x0E00, 0x0E7F, "Thai"),
    "Lao":                    (0x0E80, 0x0EFF, "Lao"),
    "Tibetan":                (0x0F00, 0x0FFF, "Tibetan"),
    "Myanmar":                (0x1000, 0x109F, "Myanmar"),
    "Georgian":               (0x10A0, 0x10FF, "Georgian"),
    "Ethiopic":               (0x1200, 0x137F, "Ethiopic"),
    "Cherokee":               (0x13A0, 0x13FF, "Cherokee"),
    "Ogham":                  (0x1680, 0x169F, "Ogham"),
    "Runic":                  (0x16A0, 0x16FF, "Runic"),
    "Tagalog":                (0x1700, 0x171F, "Tagalog"),
    "Hanunoo":                (0x1720, 0x173F, "Hanunoo"),
    "Buhid":                  (0x1740, 0x175F, "Buhid"),
    "Tagbanwa":               (0x1760, 0x177F, "Tagbanwa"),
    "Khmer":                  (0x1780, 0x17FF, "Khmer"),
    "Mongolian":              (0x1800, 0x18AF, "Mongolian"),
    "Limbu":                  (0x1900, 0x194F, "Limbu"),
    "Tai Le":                 (0x1950, 0x197F, "Tai Le"),
    "Khmer Symbols":          (0x19E0, 0x19FF, "Khmer"),
    "Greek Extended":         (0x1F00, 0x1FFF, "Greek+"),
    "Hiragana":               (0x3040, 0x309F, "Hiragana"),
    "Katakana":               (0x30A0, 0x30FF, "Katakana"),
    "CJK Unified Ideographs": (0x4E00, 0x9FFF, "CJK Ideographs"),
    "Hangul Syllables":       (0xAC00, 0xD7AF, "Korean"),
}


supported_threshold = 10


false_reports = {
    "vhsgothic": ["Hiragana", "Katakana", "Cyrillic"],
}


def determine_character_sets(font_path):
    font = TTFont(font_path)
    cmap = font["cmap"]
    unicode_maps = cmap.getBestCmap()
    supported_code_points = set(unicode_maps.keys())

    supported_sets = defaultdict(int)
    for charset_name, (start, end, simple_name) in unicode_ranges.items():
        charset_range = set(range(start, end + 1))
        overlap = supported_code_points & charset_range
        if overlap and simple_name not in false_reports.get(font_path.stem, []):
            # print(font_path, charset_name, len(overlap))
            supported_sets[simple_name] += len(overlap)

    supported = [k for k, v in supported_sets.items() if v > supported_threshold]
    supported = [s for s in supported if f"{s}+" not in supported]

    return supported


fonts_path = Path("src/ttt/resources/fonts")
for font_path in fonts_path.glob("*.ttf"):
    supported_sets = determine_character_sets(font_path)
    with open(font_path.with_suffix(".json"), "r+") as f:
        data = json.load(f)
        data["charsets"] = supported_sets
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
