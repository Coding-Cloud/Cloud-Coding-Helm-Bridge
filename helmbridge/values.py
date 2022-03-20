import os

import yaml

language_values = {'angular': 'angular-runner/values.yaml',
                   'react': 'react-runner/values.yaml'}


def get_values(language):
    return merge_dict(read_default_values(), read_language_values(language))


def read_default_values():
    with open(os.environ['INFRA_PATH'] + 'code-runner/values.yaml', 'r') as stream:
        return yaml.safe_load(stream)


def read_language_values(language):
    with open(os.environ['INFRA_PATH'] + language_values[language], 'r') as stream:
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
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a
