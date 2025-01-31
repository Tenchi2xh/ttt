from .util import Resource, load_resources, resource_getter


all_patterns: list[Resource] = load_resources("patterns.json")
all_frames: list[Resource] = load_resources("frames.json")
all_icons: list[Resource] = load_resources("icons.json")

all_patterns.sort(key=lambda p: p["height"])


get_pattern = resource_getter("pattern", all_patterns)
get_frame = resource_getter("frame", all_frames)
get_icon = resource_getter("icon", all_icons)

__all__ = [
    "all_patterns",
    "all_frames",
    "all_icons",
    "get_pattern",
    "get_frame",
    "get_icon",
    "Resource",
]
