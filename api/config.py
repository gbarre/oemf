"""API configuration module for loading settings from a YAML file."""

# Copyright (c) 2025 oemf.jrmv.net

from pathlib import Path

import yaml

from exceptions import ConfigError


class YamlConfig:
    """Configuration class for loading settings from a YAML file."""

    def __init__(self, config_file: str = "config.yaml") -> None:
        """Initialize the configuration by from a YAML file.

        Raises:
            ConfigError: If the configuration file is not found or if a
            required key is missing in the configuration file.

        """
        try:
            with Path.open(config_file) as f:
                config = yaml.full_load(f)
        except FileNotFoundError as e:
            msg = f"File {config_file} not found."
            raise ConfigError(msg) from e

        try:
            api = config["api"]
            self.HOST = api["host"]
            self.LOG_LEVEL = api["log_level"]
            self.SECRET_KEY = api["secret_key"]
            self.ENV = api["env"]

            sqlalc = api["sqlalchemy"]
            self.SQLALCHEMY_ECHO = sqlalc["echo"]
            self.SQLALCHEMY_TRACK_MODIFICATIONS = sqlalc["track_modifications"]

            # Database
            self.SQLALCHEMY_DATABASE_URI = api["database_uri"]

            self.SQLALCHEMY_ENGINE_OPTIONS = {
                # To avoid "SQL lost connection".
                "pool_pre_ping": True,
            }

            self.JWT = api["jwt"]

            self.ADMINS = api.get("admins", [])

        except KeyError as e:  # pragma: no cover
            msg = (
                f"The key `{e}` is not present in the YAML configuration file."
            )
            raise ConfigError(msg) from e
