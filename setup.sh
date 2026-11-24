#!/bin/sh
# Restore the Snowy Skips site generator into the paths the scripts expect.
# Usage: git clone -b source <repo> /home/claude/srcpkg && sh /home/claude/srcpkg/setup.sh
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
rm -rf /home/claude/site && cp -r "$HERE/site" /home/claude/site
python3 -c "import json,sys; d=json.load(open('$HERE/blobmap.json')); json.dump({k:'$HERE/'+v for k,v in d.items()}, open('/tmp/blobmap.json','w'))"
echo "Ready. Build: cd /home/claude/site && LIVE=1 python3 build_site.py && python3 -I gen_towns.py && python3 -I gen_pages.py  (output: /home/claude/website-live/)"
