import os
import shutil

from git import Repo

templates = {'angular': 'https://github.com/tomastrajan/angular-ngrx-material-starter.git'}


def create_project(project_id, language):
    cloned_repo = Repo.clone_from(templates[language], os.path.join(os.environ['REPOSITORIES_PATH'], project_id))
    print(os.listdir(os.path.join(os.environ['REPOSITORIES_PATH'], project_id)))
    print(os.listdir(os.path.join(os.environ['REPOSITORIES_PATH'])))
    print(cloned_repo)


def delete_project(project_id):
    shutil.rmtree(os.path.join('/data', project_id))
    print(os.listdir(os.path.join(os.environ['REPOSITORIES_PATH'])))
