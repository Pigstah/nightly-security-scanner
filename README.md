# Nightly Random Security Scanner


This repository demonstrates a simple **no-cost** pipeline for running static security scans on a rotating set of public GitHub repositories and publishing the aggregated results to GitHub Pages.


**Key features**
- Nightly cron-based workflow (or manual dispatch)
- Selects *N* random repos from `targets.txt` and scans them in parallel
- Uses OSS tools only (Semgrep, Trivy, Gitleaks, Checkov)
- Skips repositories that require executing untrusted code (no installs/builds)
- Aggregates JSON reports into a simple HTML dashboard and publishes to `gh-pages`


## How to use
1. Add a list of target public repos to `targets.txt` (one per line, `owner/repo` format).
2. Review and customize `.github/scripts/*` as needed.
3. Commit to a **public** GitHub repository. The workflow will run with unlimited free minutes for public repos.
4. Trigger manually via `Actions -> nightly-random-security-scan` or wait for the scheduled run.


## Security & Responsible Operation
- This project **never** installs dependencies or executes code from target repositories. Repos that require builds or installs are automatically skipped.
- The pipeline is designed for lawful, public repo scanning only. Do not use it to probe private, sensitive, or unauthorized code.


## Opt-in Emailing
This template does **not** send emails to repository owners. If you want email alerts, use an opt-in allowlist and explicit consent only.


## License
MIT