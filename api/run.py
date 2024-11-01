import argparse
import os
import uvicorn

from pathlib import Path

from app import create_app
from config import YamlConfig


parser = argparse.ArgumentParser()
parser.add_argument(
    '--config', '-c',
    dest='config_file',
    type=str,
    required=False,
    help="The YAML configuration file of the API server.",
)

# Parse only known arguments because others arguments are added during
# a DB migration.
args, unknown = parser.parse_known_args()
config_file = args.config_file

# The default YAML config file is the option is not provided.
if config_file is None:
    config_file = os.environ.get('OEMF_API_CONFIG')

if config_file is None:
    if Path('config.yml').is_file():
        config_file = 'config.yml'
    else:
        config_file = '/etc/oemf-api/config.yml'

yamlconfig = YamlConfig(config_file)
connexion_app = create_app(yamlconfig)
app = connexion_app.app

if __name__ == '__main__':
    uvicorn.run(
        f"{Path(__file__).stem}:connexion_app",
        port=5000,
    )
