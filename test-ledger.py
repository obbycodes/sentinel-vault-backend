import json
import os
import sys
from datetime import datetime

JSON_REPORT = "pytest-report.json"
LEDGER_FILE = "TEST_HISTORY.md"

if not os.path.exists(JSON_REPORT):
    print(f"Error: {JSON_REPORT} not found.")
    sys.exit(1)

with open(JSON_REPORT, "r") as f:
    data = json.load(f)

summary = data.get("summary", {})
passed = summary.get("passed", 0)
failed = summary.get("failed", 0)
skipped = summary.get("skipped", 0)
total = summary.get("total", 0)

status = "✅ PASSED" if failed == 0 and total > 0 else "❌ FAILED"
if total == 0:
    status = "⚠️ NO TESTS"

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
commit_sha = os.getenv("GITHUB_SHA", "Local Run")[:7]
run_id = os.getenv("GITHUB_RUN_ID", "")

trigger_text = f"[{commit_sha}](https://github.com{os.getenv('GITHUB_REPOSITORY')}/commit/{commit_sha})" if run_id else "Local"

# 2. Build the markdown row
new_row = f"| {timestamp} | {trigger_text} | {passed} | {failed} | {skipped} | {total} | {status} |\n"

# 3. Append row to the ledger
with open(LEDGER_FILE, "a") as f:
    f.write(new_row)

print(f"Successfully appended test run to {LEDGER_FILE}")
