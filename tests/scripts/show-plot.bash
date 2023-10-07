#!/usr/bin/env bash
D=/home/repos/euromilhoes/data

prev=
while true; do
  F=$(ls -1tr "$D"/*png 2>/dev/null | tail -1)
  [ -z "$F" ] && upd= || upd=$(stat -c "%y" "$F" 2>/dev/null)

  if [ -n "$upd" ] && [ "$upd" != "$prev" ]; then
    prev=$upd
    xdg-open "$F" &
    echo plot show updated
  fi

  sleep .5
done
