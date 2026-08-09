#!/bin/bash
cd ~/marvel-work/boot_sub
port=3700
for i in $(seq 1 120); do
  port=$((port+1))
  ~/marvel-work/python/bin/python3.10 -c "
import json, os
p = os.path.expanduser('~/marvel-work/boot_sub/launch.json')
cfg = json.load(open(p)); cfg['server_addresses'] = ['127.0.0.1:$port']
json.dump(cfg, open(p, 'w'), indent=2)"
  RELEASE=1 timeout 120 ~/marvel-work/python/bin/python3.10 ~/marvel-work/tools/test_newgame.py "~/marvel-work/boot_sub" >/dev/null 2>&1
  if grep -q "PLAYERS:" /tmp/game_stdout.log; then echo "NEWGAME OK après $((i-1)) reverts"; grep -E "SCENE CREATED|WORLD|PLAYERS|HERO" /tmp/game_stdout.log; break; fi
  bad=$(grep -oE 'source_recovered/[a-zA-Z0-9_/]+\.py' /tmp/game_stdout.log | tail -1)
  if [ -z "$bad" ]; then echo "ERREUR NON LOCALISABLE (iter $i):"; tail -15 /tmp/game_stdout.log; break; fi
  rel=${bad#source_recovered/}
  pyc="${rel%.py}.pyc"
  cp ~/marvel-work/boot/"$pyc" ~/marvel-work/boot_sub/"$pyc" || { echo "revert impossible $pyc"; break; }
  echo "revert[$i]: $rel"
done
