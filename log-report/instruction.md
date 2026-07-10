Parse `/app/access.log` (Apache Combined Log Format) and write a JSON report to `/app/report.json`.

The report must be a single JSON object with exactly two keys:

- `"status_counts"` - an object whose keys are HTTP status codes (strings, e.g. `"200"`, `"404"`) and whose values are the integer count of log lines with that status code. Include every status code that appears at least once; omit codes not present in the log.
- `"top_paths"` - an array of the 5 most-requested URL paths, sorted in descending order by request count. Each element is an object with two keys: `"path"` (string) and `"count"` (integer). If fewer than 5 distinct paths exist, include all of them.

Success criteria:

1. `/app/report.json` exists and contains valid JSON.
2. `status_counts` contains exactly the set of status codes that appear in the log, with no extras and no omissions.
3. Every count in `status_counts` equals the exact number of log lines with that status code.
4. `top_paths` lists the correct top-5 paths in strictly descending order by count, with the correct count for each path.
