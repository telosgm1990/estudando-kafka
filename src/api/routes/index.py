# Imports

from fastapi import FastAPI

from ..schemas.index import HealthcheckResponse, HelloResponse
from ..settings import Settings

# Funções


def add_index_routes(app: FastAPI, settings: Settings) -> None:
    """
    Adiciona rotas para o índice da API: /
    """

    @app.get("/")
    def hello() -> HelloResponse:
        """
        Retorna um hello world.
        """

        return HelloResponse(message="hello world")

    @app.get("/healthcheck")
    def healthcheck() -> HealthcheckResponse:
        """
        Realiza uma verificação de funcionamento e retorna o status.
        """

        return HealthcheckResponse(message="it is everything ok")
