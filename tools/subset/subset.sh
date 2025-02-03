#/bin/bash

poetry run mkdocs build

glyphhanger \
    $(find site -name "*.html" | grep -v site/overrides) \
    --subset="tools/subset/*.ttf" \
    --output=docs/fonts
