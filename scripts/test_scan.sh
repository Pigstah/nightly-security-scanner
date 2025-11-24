#!/usr/bin/env bash
set -euo pipefail

# Ensure the user passed exactly one argument
if [ "$#" -ne 1 ]; then
    echo "Usage: ./scripts/test_scan.sh <github-user/repo>"
    exit 1
fi

TARGET="$1"

echo "Cloning $TARGET..."

# Clean up previous local test directory
rm -rf local-test

# Create folders for cloned repo + results
mkdir -p local-test/results

# Shallow clone the repo (safe + fast)
git clone --depth 1 "https://github.com/$TARGET" local-test/repo

echo "Running scanner locally..."

# Run the exact same scanner the CI uses
./scripts/scan_repo.sh local-test/repo "$TARGET" local-test/results

echo "Done!"
echo "Results saved in local-test/results/"
