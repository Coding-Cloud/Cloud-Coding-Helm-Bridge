import os
import shutil

from git import Repo

from helmbridge.config import language_config


def create_project(project_id, language):
    cloned_repo = Repo.clone_from(language_config[language]['template'], os.path.join(os.environ['REPOSITORIES_PATH'], project_id))
    print(os.listdir(os.path.join(os.environ['REPOSITORIES_PATH'], project_id)))
    print(os.listdir(os.path.join(os.environ['REPOSITORIES_PATH'])))
    print(cloned_repo)


def delete_project(project_id):
    shutil.rmtree(os.path.join('/data', project_id))
    print(os.listdir(os.path.join(os.environ['REPOSITORIES_PATH'])))
