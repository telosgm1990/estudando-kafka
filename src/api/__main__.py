# Imports

import uvicorn
from loguru import logger

from src.api.bootstrap import (
    build_database_client,
    build_fastapi_app,
    build_settings,
    configure_log,
)

# Objetos globais

settings = build_settings()
database_client = build_database_client(settings)
app = build_fastapi_app(settings, database_client)

# Funções


def main() -> None:
    """
    Executa a API.
    """

    configure_log(settings)
    logger.debug(f"running api with settings (JSON): {settings.as_json()}")
    uvicorn.run(
        "src.api.__main__:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )


# Ponto de entrada

if __name__ == "__main__":
    main()
