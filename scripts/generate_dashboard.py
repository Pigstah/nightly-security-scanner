#!/usr/bin/env python3
import json
import os
import glob
from html import escape

def load_json(path):
    """Safely load JSON if file exists, else return None."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return None


def count_findings_semgrep(data):
    if not data or "results" not in data:
        return 0
    return len(data["results"])


def count_findings_gitleaks(data):
    if not data:
        return 0
    # gitleaks JSON is a list of findings
    if isinstance(data, list):
        return len(data)
    return 0


def count_findings_trivy(data):
    if not data or "Results" not in data:
        return 0
    total = 0
    for item in data["Results"]:
        vulns = item.get("Vulnerabilities", [])
        total += len(vulns)
    return total


def count_findings_checkov(data):
    if not data or "results" not in data:
        return 0
    # checkov JSON stores failures under key "failed_checks"
    return len(data.get("results", {}).get("failed_checks", []))


def make_table_row(repo_name, repo_path):
    # Detect skip
    skip_file = os.path.join(repo_path, "skip.txt")
    if os.path.exists(skip_file):
        with open(skip_file) as f:
            reason = escape(f.read())
        return f"""
            <tr>
                <td>{escape(repo_name)}</td>
                <td colspan="5"><i>Skipped: {reason}</i></td>
            </tr>
        """

    # Load tool outputs
    semgrep = load_json(os.path.join(repo_path, "semgrep.json"))
    gitleaks = load_json(os.path.join(repo_path, "gitleaks.json"))
    trivy = load_json(os.path.join(repo_path, "trivy.json"))
    checkov = load_json(os.path.join(repo_path, "checkov.json"))

    # Count findings
    semgrep_count = count_findings_semgrep(semgrep)
    gitleaks_count = count_findings_gitleaks(gitleaks)
    trivy_count = count_findings_trivy(trivy)
    checkov_count = count_findings_checkov(checkov)

    return f"""
        <tr>
            <td>{escape(repo_name)}</td>
            <td>{semgrep_count}</td>
            <td>{gitleaks_count}</td>
            <td>{trivy_count}</td>
            <td>{checkov_count}</td>
            <td><a href="{escape(repo_path)}">View Raw</a></td>
        </tr>
    """


def main(results_root):
    rows = []
    for repo_dir in sorted(os.listdir(results_root)):
        full_path = os.path.join(results_root, repo_dir)
        if os.path.isdir(full_path):
            rows.append(make_table_row(repo_dir, full_path))

    html = f"""
    <html>
    <head>
        <title>Nightly Security Scan Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 20px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid #ccc;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #eee;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
        </style>
    </head>
    <body>
        <h1>Nightly Security Scan Dashboard</h1>
        <p>This dashboard lists the results from the nightly scan across randomly selected public GitHub repositories.</p>

        <table>
            <tr>
                <th>Repository</th>
                <th>Semgrep</th>
                <th>Gitleaks</th>
                <th>Trivy</th>
                <th>Checkov</th>
                <th>Raw Output</th>
            </tr>
            {''.join(rows)}
        </table>

        <p style="margin-top: 40px;">
            <i>Generated automatically by GitHub Actions.</i>
        </p>
    </body>
    </html>
    """

    print(html)


if __name__ == "__main__":
    import sys
    main(sys.argv[1])