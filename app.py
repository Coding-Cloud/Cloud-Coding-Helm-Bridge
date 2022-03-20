import yaml
from avionix import ChartBuilder, ChartInfo, ChartDependency, Values
from flask import Flask

app = Flask(__name__)

# TODO take the repository path in body and set it in the values

@app.route('/angular/<project_id>', methods=['POST'])
def start_runner(project_id):
    try:
        with open('/home/pooetitu/Desktop/infra/code-runner/values.yaml', 'r') as stream:
            default_values = yaml.safe_load(stream)
            print(default_values)
        with open('/home/pooetitu/Desktop/infra/angular-runner/values.yaml', 'r') as stream:
            angular_values = yaml.safe_load(stream)
            print(angular_values)
        merged_values = merge(angular_values, default_values)
        print(merged_values)
        builder = ChartBuilder(
            ChartInfo(
                api_version="v2",
                name=project_id + '-angular',
                version="0.1.0",
                app_version="v1",
                dependencies=[
                    ChartDependency(
                        "code-runner",
                        "0.1.0",
                        "file:///home/pooetitu/Desktop/infra/code-runner",
                        "code-runner",
                        is_local=True,
                    ),
                ],
            ),
            [],
            values=Values({'code-runner':merged_values})
        )
        builder.install_chart({"dependency-update": None})
        return "Installed"
    except Exception as e:
        return "Failed with error " + str(e)


@app.route('/angular/<project_id>', methods=['DELETE'])
def stop_runner(project_id):
    try:
        builder = ChartBuilder(
            ChartInfo(
                api_version="v2",
                name=project_id + '-angular',
                version="0.1.0",
                app_version="v1",
            ),
            []
        )
        builder.uninstall_chart()
    except Exception as e:
        return "Failed to uninstall chart with exception " + str(e)
    return "Deleted"


def merge(a, b, path=None):
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


if __name__ == '__main__':
    app.run()
