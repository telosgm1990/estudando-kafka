# Imports

import uvicorn
from loguru import logger

from .bootstrap import build_fastapi_app, build_settings, configure_log

# Objetos globais

settings = build_settings()
app = build_fastapi_app(settings)

# Funções


def main() -> None:
    """
    Executa a API.
    """

    configure_log(settings)
    logger.debug(f"running api with settings (JSON): {settings.as_json()}")
    uvicorn.run(
        "src.api.__main__:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )


# Ponto de entrada

if __name__ == "__main__":
    main()
