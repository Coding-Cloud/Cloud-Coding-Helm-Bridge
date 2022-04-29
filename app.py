import threading

from flask import Flask, request, jsonify

from helmbridge.helm import start_code_runner, stop_code_runner
from helmbridge.project import create_project, delete_project
from helmbridge.version import get_project_versions, add_project_version, rollback_project_version

app = Flask(__name__)


@app.route('/runners/<project_id>/<language>', methods=['POST'])
def start_runner(project_id, language):
    try:
        start_code_runner(project_id, language)
        app.logger.info("Installed")
        return 'Installed\n'
    except Exception as e:
        app.logger.error(e)
        return 'Failed with error ' + str(e) + '\n'


@app.route('/runners/<project_id>', methods=['DELETE'])
def stop_runner(project_id):
    try:
        stop_code_runner(project_id)
        return 'Deleted\n'
    except Exception as e:
        app.logger.error(e)
        return 'Failed to uninstall chart with exception ' + str(e) + '\n'


@app.route('/projects/<project_id>/<language>', methods=['POST'])
def init_project(project_id, language):
    try:
        threading.Thread(target=create_project, args=(project_id, language)).start()
        return 'Project initialising\n'
    except Exception as e:
        app.logger.error(e)
        return 'Failed to create project with exception ' + str(e) + '\n'


@app.route('/projects/<project_id>', methods=['DELETE'])
def remove_project(project_id):
    try:
        delete_project(project_id)
        return 'Project deleted\n'
    except Exception as e:
        app.logger.error(e)
        return 'Failed to delete project with exception ' + str(e) + '\n'


@app.route('/versions/<project_id>', methods=['POST'])
def add_version(project_id):
    try:
        version = request.get_json()['version']
        title = request.get_json()['title']
        add_project_version(project_id, version, title)
        return 'Version added\n'
    except Exception as e:
        app.logger.error(e)
        return 'Failed to add the version with exception ' + str(e) + '\n'


@app.route('/versions/<project_id>', methods=['GET'])
def list_versions(project_id):
    try:
        return jsonify(get_project_versions(project_id))
    except Exception as e:
        app.logger.error(e)
        return 'Failed to get project versions with exception ' + str(e) + '\n'


@app.route('/versions/<project_id>/<versions>', methods=['PATCH'])
def rollback_version(project_id, versions):
    try:
        rollback_project_version(project_id, versions)
        return 'Project rollback succeeded\n'
    except Exception as e:
        app.logger.error(e)
        return 'Failed to rollback the version with exception ' + str(e) + '\n'


if __name__ == '__main__':
    app.run()
