"""API application module."""

# Copyright (c) 2025 oemf.jrmv.net

import logging
from pathlib import Path
from typing import Any

import connexion
import prance
from connexion import FlaskApp
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from starlette.middleware.cors import CORSMiddleware

from config import YamlConfig

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
cors = CORS()


def get_bundled_specs(main_file: Path) -> dict[str, Any]:
    """Load and parse the OpenAPI specification from a bundled YAML file.

    Returns:
        dict[str, Any]: The parsed OpenAPI specification as a dictionary.

    """
    parser = prance.ResolvingParser(
        str(main_file.absolute()),
        lazy=True,
        strict=True,
    )
    parser.parse()
    spec = parser.specification

    for path, methods in list(spec.get("paths", {}).items()):
        for method, details in list(methods.items()):
            if isinstance(details, dict) and details.get("x-hide", False):
                del spec["paths"][path][method]
        if not spec["paths"][path]:
            del spec["paths"][path]

    return spec


def create_app(config: YamlConfig) -> FlaskApp:
    """Create and configure the Flask application with Connexion and CORS.

    Returns:
        FlaskApp: The configured Connexion application instance.

    """
    connexion_app = FlaskApp(__name__)

    connexion_app.add_middleware(
        CORSMiddleware,
        position=connexion.middleware.MiddlewarePosition.BEFORE_EXCEPTION,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Total-Count", "X-Limit", "X-Offset"],
    )
    connexion_app.add_api(
        get_bundled_specs(
            Path("spec/index.yml"),
        ),
        resolver=connexion.resolver.RelativeResolver("endpoints"),
        strict_validation=False,
        validate_responses=True,
    )
    app = connexion_app.app
    app.config.from_object(config)

    class SkipOptionsFilter(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:  # noqa: PLR6301
            """Filter out OPTIONS requests from the logs.

            Returns:
                bool: True if the log record should be logged,
                False if it should be skipped.

            """
            return "OPTIONS" not in record.getMessage()

    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
    uvicorn_access_logger.addFilter(SkipOptionsFilter())
    app.logger.handlers = uvicorn_access_logger.handlers
    app.logger.setLevel(config.LOG_LEVEL)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    cors.init_app(app)
    return connexion_app
