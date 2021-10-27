import os
import json
import shutil
import argparse
from git import Repo
from datetime import datetime

date_key = datetime.today().strftime('%d-%m-%Y')

username = "TennisGazelle"
password = ""
reponame = "isitabonesday"
remote = f"https://{username}:{password}@github.com/{username}/{reponame}.git"
local_path = f"../tmp/{reponame}"
history_file_path = f"{local_path}/history.json"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=f'Update isitabonesday.com for {date_key}')
    parser.add_argument('-b', '--bones', action='store_const', const=True, default=False)
    parser.add_argument('-r', '--rest', action='store_const', const=True, default=False)
    args = parser.parse_args()
    print(date_key, args.bones)

    # clone repo
    if os.path.exists(local_path):
        shutil.rmtree(local_path)
    Repo.clone_from(url=remote, to_path=local_path)
    
    git_repo = Repo(local_path)
    git_repo.git.checkout("master")
    print(git_repo.git.status())

    # read
    with open(history_file_path, 'r') as history_file:
        history = json.loads(history_file.read())
        history_file.close()

    # update
    history[date_key] = {
        "bones": args.bones,
        "rest": args.rest,
    }

    # write
    with open(history_file_path, 'w') as history_file:
        history_file.write(json.dumps(history, indent=3))
        history_file.close()
    print(git_repo.git.status())

    # push it up to master
    git_repo.git.add(os.path.abspath(history_file_path))
    git_repo.git.commit(m=f"update for {date_key}")
    git_repo.git.push('--set-upstream', 'origin', 'master')
