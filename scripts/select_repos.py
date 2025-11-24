#!/usr/bin/env python3
import requests
import random
import json
import re

# Number of repos per run
COUNT = 10


def sanitize_repo_name(name: str) -> str:
    """
    Replace slashes with dots so repo names are safe for
    GitHub Actions artifact paths.
    Example: 'owner/repo' -> 'owner.repo'
    """
    return name.replace("/", ".")


def get_random_repos(count=COUNT):
    """
    Use GitHub Search API to fetch trending/popular repos.
    We avoid forks, archived repos, and huge repos by filtering.
    """
    url = "https://api.github.com/search/repositories"
    params = {
        "q": "stars:>100 language:python language:javascript language:go",
        "sort": "stars",
        "order": "desc",
        "per_page": 100,
    }

    r = requests.get(url, params=params)
    data = r.json()

    repos = [item["full_name"] for item in data.get("items", [])]
    random.shuffle(repos)

    return repos[:count]


if __name__ == "__main__":
    repos = get_random_repos()

    # Add sanitized names to the GitHub Actions matrix
    matrix = {
        "include": [
            {
                "repo": r,
                "safe_repo": sanitize_repo_name(r)
            }
            for r in repos
        ]
    }

    print(json.dumps(matrix))
