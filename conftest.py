import os

os.environ['SETTINGS_MODULE'] = 'test'

pytest_plugins = ["docker_compose"]
