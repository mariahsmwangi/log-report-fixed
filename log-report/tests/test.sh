#!/usr/bin/env bash
# Run the pytest verifier and write reward.txt + ctrf.json to /logs/verifier/.
set -euo pipefail

LOG_DIR="/logs/verifier"
mkdir -p "$LOG_DIR"

# Run pytest; capture exit code without failing the script immediately.
set +e
pytest /app/tests/test_outputs.py \
    --json-report --json-report-file="$LOG_DIR/ctrf.json" \
    -v 2>&1
EXIT_CODE=$?
set -e

# Write reward: 1 if all tests passed, 0 otherwise.
if [ "$EXIT_CODE" -eq 0 ]; then
    echo "1" > "$LOG_DIR/reward.txt"
else
    echo "0" > "$LOG_DIR/reward.txt"
fi

exit 0
