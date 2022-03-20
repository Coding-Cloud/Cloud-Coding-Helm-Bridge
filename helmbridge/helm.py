import os

from avionix import ChartBuilder, ChartInfo, ChartDependency, Values

from helmbridge.values import get_values


def start_code_runner(project_id, language, repository_path):
    merged_values = get_values(language, repository_path)
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
                    'file://' + os.environ['INFRA_PATH'] + '/code-runner',
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
