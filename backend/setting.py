import yaml
import requests
import base64
from pathlib import Path
import os

root_dir = os.path.dirname(__file__)
config_path = Path(root_dir) / 'config.yaml'

def load_config(config_path):
    configs = dict()
    with open(config_path, 'r') as file:
        yaml_data = yaml.safe_load(file)

    configs.update(yaml_data)
    return configs

configs = load_config(root_dir/Path('config.yaml'))

# Prefer the OPENAI_API_KEY environment variable over config.yaml (secure practice).
# Never commit real API keys to version control.
env_api_key = os.environ.get('OPENAI_API_KEY')
if env_api_key:
    configs['api_key'] = env_api_key

if __name__ == '__main__':
    print(config_path)
    for key, value in configs.items():
        print(key, ':', value)