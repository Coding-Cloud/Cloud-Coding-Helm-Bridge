from flask import Flask, request

from helmbridge.helm import start_code_runner, stop_code_runner

app = Flask(__name__)


@app.route('/<project_id>/<language>', methods=['POST'])
def start_runner(project_id, language):
    try:
        start_code_runner(project_id, language)
        return 'Installed'
    except Exception as e:
        return 'Failed with error ' + str(e)


@app.route('/<project_id>', methods=['DELETE'])
def stop_runner(project_id):
    try:
        stop_code_runner(project_id)
        return 'Deleted'
    except Exception as e:
        return 'Failed to uninstall chart with exception ' + str(e)


if __name__ == '__main__':
    app.run()
