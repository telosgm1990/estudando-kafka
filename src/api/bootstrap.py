# Imports

import sys
from fastapi import FastAPI
from loguru import logger

from src.api.repositories.user import UsersRepository
from src.api.routes.auth import add_auth_routes
from src.api.routes.index import add_index_routes
from src.common.database.client import DatabaseClient
from src.common.settings import Settings

# Funções


def build_settings() -> Settings:
    """
    Constroi o objeto de configurações.
    """

    return Settings.from_env_file(".env")


def build_database_client(settings: Settings) -> DatabaseClient:
    """
    Constroi o client para o banco de dados.
    """

    return DatabaseClient(settings)


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
        "eligibilityloader/{time:YYYYMMDD}/{time:HHmmssSS}.log"
    )
    logger.remove()
    logger.add(sys.stderr, level=logger_level)
    logger.add(str(logger_sink_path), level=logger_level)
