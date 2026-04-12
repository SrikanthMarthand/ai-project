from wsgiref import headers

import requests

def get_commit_details(owner, repo, sha):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}"

    import os
    headers = {
    "Authorization": f"token {os.getenv('GITHUB_TOKEN')}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    data = response.json()

    files = data.get("files", [])

    activities = []

    for f in files:
        activities.append({
            "file_name": f.get("filename", "unknown"),
            "additions": f.get("additions", 0),
            "deletions": f.get("deletions", 0)
        })

    return activities