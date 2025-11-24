#!/usr/bin/env python3
import json
from select_repos import get_random_repos

# Call the real selection function
repos = get_random_repos()

# Pretty-print the selected repos
print("\nSelected repos:")
for r in repos:
    print("  -", r)

# Format the matrix exactly like the GitHub workflow will see it
print("\nMatrix JSON:")
matrix = {"include": [{"repo": r} for r in repos]}
print(json.dumps(matrix, indent=2))
