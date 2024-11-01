import connexion
import logging
import prance

from connexion import FlaskApp
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from typing import Any, Dict


db = SQLAlchemy()
migrate = Migrate()


def get_bundled_specs(main_file: Path) -> Dict[str, Any]:
    parser = prance.ResolvingParser(
        str(main_file.absolute()),
        lazy=True,
        strict=True,
    )
    parser.parse()
    return parser.specification


def create_app(config):
    connexion_app = FlaskApp(__name__)

    connexion_app.add_api(
        get_bundled_specs(
            Path("spec/index.yml"),
        ),
        resolver=connexion.resolver.RelativeResolver('endpoints'),
        strict_validation=False,
        validate_responses=True,
    )

    app = connexion_app.app
    app.config.from_object(config)

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(config.LOG_LEVEL)

    db.init_app(app)
    migrate.init_app(app, db)
    return connexion_app
