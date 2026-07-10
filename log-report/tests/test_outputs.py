import json
import os
import collections

REPORT_PATH = "/app/report.json"
LOG_PATH    = "/app/access.log"


def _parse_log(log_path):
    """Return (status_counts, top_paths) computed directly from the log."""
    status_counts = collections.Counter()
    path_counts   = collections.Counter()
    with open(log_path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            parts = line.split('"')
            if len(parts) < 2:
                continue
            request_parts = parts[1].split()
            if len(request_parts) < 2:
                continue
            path = request_parts[1]
            after_request = parts[2].split()
            if not after_request:
                continue
            status = after_request[0]
            status_counts[status] += 1
            path_counts[path]     += 1
    top_paths = [
        {"path": p, "count": c}
        for p, c in path_counts.most_common(5)
    ]
    return dict(status_counts), top_paths


def test_report_is_valid_json():
    """Criterion 1: /app/report.json exists and is valid JSON."""
    assert os.path.exists(REPORT_PATH), f"{REPORT_PATH} was not created"
    with open(REPORT_PATH) as fh:
        data = json.load(fh)
    assert isinstance(data, dict), "report.json must be a JSON object"


def test_status_counts_keys():
    """Criterion 2: status_counts contains exactly the status codes in the log."""
    with open(REPORT_PATH) as fh:
        data = json.load(fh)
    expected_counts, _ = _parse_log(LOG_PATH)
    assert "status_counts" in data, "Missing key 'status_counts'"
    assert set(data["status_counts"].keys()) == set(expected_counts.keys())


def test_status_counts_values():
    """Criterion 3: Each status-code count matches the actual count in the log."""
    with open(REPORT_PATH) as fh:
        data = json.load(fh)
    expected_counts, _ = _parse_log(LOG_PATH)
    for code, expected_val in expected_counts.items():
        actual_val = data["status_counts"].get(code)
        assert actual_val == expected_val, f"Status {code}: expected {expected_val}, got {actual_val}"


def test_top_paths_correct_and_ordered():
    """Criterion 4: top_paths lists the top-5 paths sorted descending by count."""
    with open(REPORT_PATH) as fh:
        data = json.load(fh)
    _, expected_top = _parse_log(LOG_PATH)
    assert "top_paths" in data, "Missing key 'top_paths'"
    actual = data["top_paths"]
    assert isinstance(actual, list), "'top_paths' must be a JSON array"
    assert len(actual) == len(expected_top)
    for i, (act, exp) in enumerate(zip(actual, expected_top)):
        assert act.get("path") == exp["path"], f"top_paths[{i}] path mismatch"
        assert act.get("count") == exp["count"], f"top_paths[{i}] count mismatch"
