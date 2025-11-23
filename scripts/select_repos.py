#!/usr/bin/env python3
import requests
import random
import json

# Number of repos per run
COUNT = 10


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

    # Format GitHub Actions matrix output
    matrix = {"include": [{"repo": r} for r in repos]}
    print(json.dumps(matrix))
