import yaml
from exceptions import ConfigError


class YamlConfig:

    def __init__(self, config_file):
        try:
            with open(config_file) as f:
                config = yaml.full_load(f)
        except FileNotFoundError:
            raise ConfigError(f"File {config_file} not found.")

        try:
            api = config['api']
            self.HOST = api['host']
            self.LOG_LEVEL = api['log_level']
            self.SECRET_KEY = api['secret_key']
            self.ENV = api['env']

            sqlalc = api['sqlalchemy']
            self.SQLALCHEMY_ECHO = sqlalc['echo']
            self.SQLALCHEMY_TRACK_MODIFICATIONS = sqlalc['track_modifications']

            # Database
            self.SQLALCHEMY_DATABASE_URI = api['database_uri']

            self.SQLALCHEMY_ENGINE_OPTIONS = {
                # To avoid "SQL lost connection".
                'pool_pre_ping': True,
            }

        except KeyError as e:  # pragma: no cover
            raise ConfigError(
                f"The key `{e}` is not present in the YAML configuration file."
            )
