import os

from git import Repo


def add_project_version(project_id, version, title):
    repo = Repo(os.path.join(os.environ['REPOSITORIES_PATH'], project_id))
    repo.index.add('.')
    repo.index.commit('{version} - {title}'.format(version=version, title=title))


def get_project_versions(project_id):
    repo = Repo(os.path.join(os.environ['REPOSITORIES_PATH'], project_id))
    return [commit.message for commit in repo.iter_commits(rev=repo.head.reference)]


def rollback_project_version(project_id, versions=1):
    repo = Repo(os.path.join(os.environ['REPOSITORIES_PATH'], project_id))
    repo.head.reset('--hard HEAD~versions'.format(versions), index=True, working_tree=True)
