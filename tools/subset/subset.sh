#/bin/bash

glyphhanger \
    $(find site -name "*.html" | grep -v site/overrides) \
    --subset="tools/subset/*.ttf" \
    --family="Iosevka Kotan Term" \
    --output=docs/fonts \
    --css
