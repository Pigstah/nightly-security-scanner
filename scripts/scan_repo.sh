#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$1"
REPO_NAME="$2"
OUT_DIR="$3"

mkdir -p "$OUT_DIR"

echo "Scanning $REPO_NAME in $REPO_DIR"

##############################################
# 1. SAFE SKIP RULES (no execution allowed)
##############################################

if [ -f "$REPO_DIR/Makefile" ] \
  || [ -f "$REPO_DIR/pom.xml" ] \
  || [ -f "$REPO_DIR/build.gradle" ] \
  || [ -f "$REPO_DIR/package.json" ]; then
    echo "SKIP: $REPO_NAME requires build/execution" | tee "$OUT_DIR/skip.txt"
    exit 0
fi

if ! find "$REPO_DIR" -type f \( \
     -name "*.py" -o -name "*.js" -o -name "*.ts" -o \
     -name "*.go" -o -name "*.rb" -o -name "*.php" \
   \) | grep -q . ; then
    echo "SKIP: $REPO_NAME has no supported source files" | tee "$OUT_DIR/skip.txt"
    exit 0
fi

##############################################
# 2. RUN SEMGREP (Static Code Analysis)
##############################################
echo "Running Semgrep..."
semgrep --config=auto "$REPO_DIR" --json --disable-version-check 2>&1 \
  | awk 'BEGIN {found=0} /^\{/ {found=1} found {print}' \
  | jq '.' > "$OUT_DIR/semgrep.json" \
  || echo "Semgrep crashed" > "$OUT_DIR/semgrep_error.txt"


##############################################
# 3. RUN GITLEAKS
##############################################
echo "Running Gitleaks..."
gitleaks detect --source "$REPO_DIR" --no-banner \
    --report-format json --report-path "$OUT_DIR/gitleaks.json" \
    --exit-code 0 \
    || echo "Gitleaks crashed" > "$OUT_DIR/gitleaks_error.txt"


##############################################
# 4. RUN TRIVY
##############################################
echo "Running Trivy FS..."
trivy fs "$REPO_DIR" --quiet --format json \
    --output "$OUT_DIR/trivy.json" \
    --exit-code 0 \
    || echo "Trivy crashed" > "$OUT_DIR/trivy_error.txt"


##############################################
# 5. RUN CHECKOV
##############################################
echo "Running Checkov..."
checkov -d "$REPO_DIR" -o json > "$OUT_DIR/checkov.json" \
    || echo "Checkov crashed" > "$OUT_DIR/checkov_error.txt"


echo "Scan completed for $REPO_NAME"
exit 0
