import subprocess
from time import sleep
import os


def download_user(user):
    file = f"dataset/tweets/{user}-tweets.jsonl"
    if not os.path.exists(file):
        command = [
            "twarc2",
            "timeline",
            "--exclude-replies",
            "--exclude-retweets",
            "--hide-progress",
            user,
            file,
        ]
        subprocess.run(command)
        return True
    else:
        return False


users = [line.strip() for line in open("dataset/accounts.txt").readlines() if line.strip()]

for user in users:
    print(f"Downloading {user}")
    if download_user(user):
        sleep(120)
