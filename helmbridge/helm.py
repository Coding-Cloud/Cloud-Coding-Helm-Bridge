import os

from avionix import ChartBuilder, ChartInfo, ChartDependency, Values
from flask import Flask

from helmbridge.values import get_values

logger = Flask(__name__).logger


def start_code_runner(project_id, language):
    merged_values = get_values(language, project_id)
    builder = ChartBuilder(
        ChartInfo(
            api_version='v2',
            name=project_id,
            version='0.1.0',
            app_version='v1',
            dependencies=[
                ChartDependency(
                    'code-runner',
                    '0.1.0',
                    'file://' + os.environ['CODE_RUNNER_PATH'],
                    'code-runner',
                    is_local=True,
                ),
            ],
        ),
        [],
        values=Values({'code-runner': merged_values})
    )
    builder.install_chart({'dependency-update': None})


def stop_code_runner(project_id):
    builder = ChartBuilder(
        ChartInfo(
            api_version='v2',
            name=project_id,
            version='0.1.0',
            app_version='v1',
        ),
        []
    )
    builder.uninstall_chart()
