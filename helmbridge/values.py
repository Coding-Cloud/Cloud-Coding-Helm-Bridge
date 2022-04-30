import os

import yaml

from helmbridge.config import language_config


def get_values(language, project_id):
    values = merge_dict(read_default_values(), read_language_values(language))
    values['project']['id'] = project_id
    return values


def read_default_values():
    with open(os.path.join(os.environ['VALUES_PATH'], 'code-runner-values.yaml'), 'r') as stream:
        return yaml.safe_load(stream)


def read_language_values(language):
    with open(os.path.join(os.environ['VALUES_PATH'], language_config[language]['values']), 'r') as stream:
        return yaml.safe_load(stream)


def merge_dict(a, b, path=None):
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dict(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a
