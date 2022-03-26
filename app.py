import asyncio
import threading

from flask import Flask

from helmbridge.helm import start_code_runner, stop_code_runner
from helmbridge.project import create_project, delete_project

app = Flask(__name__)


@app.route('/runner/<project_id>/<language>', methods=['POST'])
def start_runner(project_id, language):
    try:
        start_code_runner(project_id, language)
        return 'Installed\n'
    except Exception as e:
        return 'Failed with error ' + str(e) + '\n'


@app.route('/runner/<project_id>', methods=['DELETE'])
def stop_runner(project_id):
    try:
        stop_code_runner(project_id)
        return 'Deleted\n'
    except Exception as e:
        return 'Failed to uninstall chart with exception ' + str(e) + '\n'


@app.route('/project/<project_id>/<language>', methods=['POST'])
def init_project(project_id, language):
    try:
        threading.Thread(target=create_project, args=(project_id, language)).start()
        return 'Project initialising\n'
    except Exception as e:
        return 'Failed to create project with exception ' + str(e) + '\n'


@app.route('/project/<project_id>', methods=['DELETE'])
def remove_project(project_id):
    try:
        delete_project(project_id)
        return 'Project deleted\n'
    except Exception as e:
        return 'Failed to delete project with exception ' + str(e) + '\n'


if __name__ == '__main__':
    app.run()
