import os
import shutil

import requests
from flask import Flask
from git import Repo

from helmbridge.config import language_config

logger = Flask(__name__).logger


def create_project(project_id, language, repo_url):
    try:
        repo_url = language_config[language]['template'] if not repo_url else repo_url
        repo_path = os.path.join(os.environ['REPOSITORIES_PATH'], project_id)
        Repo.clone_from(repo_url, repo_path)
        shutil.rmtree(os.path.join(repo_path, '.git'))
        repo = Repo.init(repo_path)
        repo.git.add(all=True)
        repo.index.commit('1 - Initial version')
        requests.patch(os.environ['API_URL'] + 'projects/' + project_id + '/initialised')
        os.system('chmod -R 777 ' + repo_path)
    except Exception as e:
        logger.error(e)


def delete_project(project_id):
    shutil.rmtree(os.path.join(os.environ['REPOSITORIES_PATH'], project_id))
