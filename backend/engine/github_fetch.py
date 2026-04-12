import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"token {TOKEN}"
}

def fetch_commits(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    res = requests.get(url, headers=HEADERS)
    return res.json()