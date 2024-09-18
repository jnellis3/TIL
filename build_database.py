from bs4 import BeautifulSoup
from datetime import timezone
import httpx
import git
import os
import pathlib
from urllib.parse import urlencode
import sqlite_utils
from sqlite_utils.db import NotFoundError
import time

root = pathlib.Path(__file__).parent.resolve()

def first_paragraph_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return " ".join(soup.find("p").stripped_strings)

def created_changed_times(repo_path, ref="main"):
    created_changed_times = {}
    repo = git.Repo(repo_path, odbt=git.GitDB)
    commits = reversed(list(repo.iter_commits(ref)))
    for commit in commits:
        dt = commit.committed_datetime
        affected_files = list(commit.stats.files.keys())
        for filepath in affected_files:
            if filepath not in created_changed_times:
                created_changed_times[filepath] = {
                    "created": dt.isoformat(),
                    "created_utc": dr.astimezone(timezone.utc)
                }
            created_changed_times[filepath].update(
                {
                    "updated": dt.isoformat(),
                    "updated_utc": dt.astimezone(timezone.utc).isoformat()
                }
            )
    return created_changed_times

def build_database(repo_path):
    db = sqlite_utils.Database(repo_path / "tils.db")
    all_times = created_changed_times(repo_path)

if __name__ == "__main__":
    build_database(root)
    print('Hello World')
