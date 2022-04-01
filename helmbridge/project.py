import os
import shutil

import requests
from git import Repo

from helmbridge.config import language_config


def create_project(project_id, language):
    repo = Repo.clone_from(language_config[language]['template'],
                           os.path.join(os.environ['REPOSITORIES_PATH'], project_id))
    repo.init()
    repo.index.add('.')
    repo.index.commit('1 - Initial version')
    requests.patch(os.environ['API_URL'] + '/projects/' + project_id + '/initialised')


def delete_project(project_id):
    shutil.rmtree(os.path.join('/data', project_id))
