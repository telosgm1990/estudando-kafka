# Imports

import sys
from fastapi import FastAPI
from loguru import logger

from .routes.index import add_index_routes
from .settings import Settings

# Funções


def build_settings() -> Settings:
    """
    Constroi o objeto de configurações.
    """

    settings = Settings.from_cli_args()
    return settings


def build_fastapi_app(settings: Settings) -> FastAPI:
    """
    Constroi o objeto FastAPI.
    """

    # Construa o objeto FastAPI
    app = FastAPI()
    # Adicione as rotas
    add_index_routes(app, settings)
    # Retorne o objeto FastAPI
    return app


def configure_log(settings: Settings) -> None:
    """
    Configura os logs.
    """

    logger_level = settings.log_level.upper()
    logger_sink_path = settings.log_directory_path.joinpath(
        "/eligibilityloader/{time:YYYYMMDD}/{time:HHmmssSS}.log"
    )
    logger.remove()
    logger.add(sys.stderr, level=logger_level)
    logger.add(str(logger_sink_path), level=logger_level)
