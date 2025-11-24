#!/usr/bin/env python3
import os
import json
from generate_dashboard import main

"""
This script builds a test dashboard using dummy results.

Useful because:
  - You don't need to run any real scans
  - You can see how the HTML page looks
  - You can debug layout, styling, and logic offline
"""

# Create fake result folders
os.makedirs("dummy-results/repo1", exist_ok=True)
os.makedirs("dummy-results/repo2", exist_ok=True)
os.makedirs("dummy-results/repo3", exist_ok=True)

# Repo 1: normal results
with open("dummy-results/repo1/semgrep.json", "w") as f:
    json.dump({"results": [{"id": 1}, {"id": 2}]}, f)

with open("dummy-results/repo1/gitleaks.json", "w") as f:
    json.dump([{"secret": "x"}, {"secret": "y"}], f)

with open("dummy-results/repo1/trivy.json", "w") as f:
    json.dump({"Results": [{"Vulnerabilities": [{"id": "CVE-123"}]}]}, f)

with open("dummy-results/repo1/checkov.json", "w") as f:
    json.dump({"results": {"failed_checks": [{"id": 1}]}}, f)

# Repo 2: show how "skipped" appears
with open("dummy-results/repo2/skip.txt", "w") as f:
    f.write("Repo required build execution")

# Repo 3: empty repo (no results)
# Folder already exists; leaving it empty simulates a failure or zero-output repo

print("Generating dashboard from dummy data...\n")

# Generate HTML
main("dummy-results")
