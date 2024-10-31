import prance
import connexion

from typing import Any, Dict
from pathlib import Path

from connexion import AsyncApp


def get_bundled_specs(main_file: Path) -> Dict[str, Any]:
    parser = prance.ResolvingParser(
        str(main_file.absolute()),
        lazy=True,
        strict=True,
    )
    parser.parse()
    return parser.specification

connexion_app = AsyncApp(__name__)

connexion_app.add_api(
    get_bundled_specs(
        Path("spec/index.yml"),
    ),
    resolver=connexion.RestyResolver("rest_api"),
    strict_validation=False,
    validate_responses=True,
)
