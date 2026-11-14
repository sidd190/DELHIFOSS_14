#!/usr/bin/env bash
set -eu
cd -- "$(dirname -- "$0")"
if command -v python3 >/dev/null 2>&1; then
  exec python3 scripts/serve.py
fi
# This workstation uses Nix and does not expose Python on PATH.
for talk_python in /nix/store/*python3-3.12.*/bin/python3 /nix/store/*python3-3.13.*/bin/python3; do
  if [ -x "$talk_python" ]; then exec "$talk_python" scripts/serve.py; fi
done
echo 'Install Python 3.10+ and run: python3 scripts/serve.py' >&2
exit 1
