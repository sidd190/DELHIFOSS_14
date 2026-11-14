#!/usr/bin/env bash
set -eu
cd -- "$(dirname -- "$0")"
if command -v python3 >/dev/null 2>&1; then
  exec python3 -m unittest discover -s tests -v
fi
for talk_python in /nix/store/*python3-3.12.*/bin/python3 /nix/store/*python3-3.13.*/bin/python3; do
  if [ -x "$talk_python" ]; then exec "$talk_python" -m unittest discover -s tests -v; fi
done
echo 'Python 3.10+ required' >&2
exit 1
