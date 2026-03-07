#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-4173}"
OUTPUT_FILE="$(mktemp)"

cleanup() {
  if [[ -n "${SERVER_PID:-}" ]]; then
    kill "${SERVER_PID}" >/dev/null 2>&1 || true
    wait "${SERVER_PID}" 2>/dev/null || true
  fi
  rm -f "${OUTPUT_FILE}"
}

trap cleanup EXIT

cd "${ROOT_DIR}"
python3 -m http.server "${PORT}" --bind "${HOST}" >/tmp/linguist-browser-tests.log 2>&1 &
SERVER_PID=$!

for _ in $(seq 1 50); do
  if curl -sSf "http://${HOST}:${PORT}/tests/browser_suite.html" >/dev/null 2>&1; then
    break
  fi
  sleep 0.2
done

SUITE_URL="http://${HOST}:${PORT}/tests/browser_suite.html"

google-chrome \
  --headless \
  --disable-gpu \
  --no-sandbox \
  --autoplay-policy=no-user-gesture-required \
  --virtual-time-budget=12000 \
  --dump-dom "${SUITE_URL}" >"${OUTPUT_FILE}"

cat "${OUTPUT_FILE}"

if grep -q 'data-suite-status="fail"' "${OUTPUT_FILE}"; then
  exit 1
fi

if ! grep -q 'data-suite-status="pass"' "${OUTPUT_FILE}"; then
  echo "Test runner did not report a final status." >&2
  exit 1
fi
