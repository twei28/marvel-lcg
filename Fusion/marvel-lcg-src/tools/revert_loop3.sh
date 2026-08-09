#!/bin/bash
cd ~/marvel-work/boot_sub
port=3400
for i in $(seq 1 60); do
  port=$((port+1))
  RELEASE=1 timeout 120 ~/marvel-work/python/bin/python3.10 /tmp/test_server_port.py $port >/dev/null 2>&1
  if grep -q "SCENE HTTP 200" /tmp/game_stdout.log; then echo "SCENE OK après $((i-1)) reverts"; break; fi
  bad=$(grep -oE 'source_recovered/[a-zA-Z0-9_/]+\.py' /tmp/game_stdout.log | tail -1)
  if [ -z "$bad" ]; then echo "ERREUR NON LOCALISABLE (iter $i):"; tail -12 /tmp/game_stdout.log; break; fi
  rel=${bad#source_recovered/}
  pyc="${rel%.py}.pyc"
  cp ~/marvel-work/boot/"$pyc" ~/marvel-work/boot_sub/"$pyc" || { echo "revert impossible $pyc"; break; }
  echo "revert[$i]: $rel"
done
