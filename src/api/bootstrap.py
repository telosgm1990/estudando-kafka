# Imports

import sys
from fastapi import FastAPI
from loguru import logger

from src.common.database.client import DatabaseClient

from .repositories.user import UsersRepository
from .routes.auth import add_auth_routes
from .routes.index import add_index_routes
from .settings import Settings

# Funções


def build_settings() -> Settings:
    """
    Constroi o objeto de configurações.
    """

    settings = Settings.from_cli_args()
    return settings


def build_database_client() -> DatabaseClient:
    """
    Constroi o client para o banco de dados.
    """

    return DatabaseClient()


def build_fastapi_app(
    settings: Settings, database_client: DatabaseClient
) -> FastAPI:
    """
    Constroi o objeto FastAPI.
    """

    # Construa o objeto FastAPI
    app = FastAPI()
    # Construa os objetos para repositórios
    users_repo = UsersRepository(database_client)
    # Adicione as rotas
    add_index_routes(app, settings)
    add_auth_routes(app, settings, users_repo)
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
