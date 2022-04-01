import os
import shutil

import requests
from git import Repo

from helmbridge.config import language_config


def create_project(project_id, language):
    repo_path = os.path.join(os.environ['REPOSITORIES_PATH'], project_id)
    Repo.clone_from(language_config[language]['template'], repo_path)
    shutil.rmtree(os.path.join(repo_path, '.git'))
    repo = Repo.init(repo_path)
    repo.index.add('.')
    repo.index.commit('1 - Initial version')
    requests.patch(os.environ['API_URL'] + '/projects/' + project_id + '/initialised')


def delete_project(project_id):
    shutil.rmtree(os.path.join(os.environ['REPOSITORIES_PATH'], project_id))
