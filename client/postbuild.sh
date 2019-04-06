#!/usr/bin/env bash
# sed in macOS is different from the one in Linux, cannot use sed -i
# sed 's/fonts.googleapis.com/fonts.loli.net/g' dist/index.html > dist/index.html_replaced
# mv dist/index.html_replaced dist/index.html
cp src/assets/logo.png dist/favicon.ico