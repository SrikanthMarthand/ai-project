def parse_commits(commits):
    activities = []

    for c in commits[:5]:
        activities.append({
            "developer_id": c["commit"]["author"]["name"],
            "file_name": "repo_file",
            "start_line": 1,
            "end_line": 20,
            "timestamp": c["commit"]["author"]["date"],
            "additions": 0,
            "deletions": 0,
            "commit_message": c["commit"]["message"]
        })

    return activities