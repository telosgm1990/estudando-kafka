# Imports

import json
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Final, NamedTuple, Literal

from pydantic import BaseModel as PydanticBaseModel

from src.common.settings import PROJECT_ROOT_PATH

# Tipos

LogLevel = Literal["debug", "info"]

# Constantes globais

LOG_LEVEL_DEFAULT: Final[LogLevel] = "info"
LOG_DIRECTORY_DEFAULT_PATH: Final[Path] = PROJECT_ROOT_PATH.joinpath(".logs")

HOST_DEFAULT: Final[str] = "127.0.0.1"
PORT_DEFAULT: Final[int] = 8037
RELOAD_DEFAULT: Final[bool] = False


# Classes


class Settings(PydanticBaseModel):
    """
    Configurações da API.
    """

    log_level: LogLevel
    log_directory: str
    host: str
    port: int
    reload: bool

    @property
    def log_directory_path(self) -> Path:
        """
        Retorna um objeto Path para o diretório de logs.
        """
        return Path(self.log_directory).absolute()

    @classmethod
    def from_cli_args(cls) -> "Settings":
        """
        Constroi o objeto de configurações utilizando os argumentos da linha de
        comando.
        """

        kwargs = cls._build_kwargs()
        return cls(**kwargs)

    def as_json(self) -> str:
        """
        Returna o objeto de configurações em formato string JSON.
        """

        return self.model_dump_json()

    @staticmethod
    def _build_kwargs() -> dict[str, Any]:
        default_log_directory_path = PROJECT_ROOT_PATH.joinpath(".logs")
        default_log_directory_path.mkdir(exist_ok=True)
        argument_parser = ArgumentParser(
            "EstudandoKafkaAPI", description="Executa a API EstudandoKafka"
        )
        argument_parser.add_argument(
            "--log-level",
            type=str,
            default=LOG_LEVEL_DEFAULT,
            choices=("debug", "info"),
            help="Menor nível de LOG a ser exibido.",
        )
        argument_parser.add_argument(
            "--log-directory",
            type=str,
            default=str(LOG_DIRECTORY_DEFAULT_PATH),
            help="Caminho onde serão armazenados os logs.",
        )
        argument_parser.add_argument(
            "--host",
            type=str,
            default=HOST_DEFAULT,
            help="Endereço IP do host.",
        )
        argument_parser.add_argument(
            "--port", type=int, default=PORT_DEFAULT, help="Porta do host."
        )
        argument_parser.add_argument(
            "--reload",
            type=bool,
            default=RELOAD_DEFAULT,
            help="Se a API deve reiniciar caso algo arquivo seja editado.",
        )
        return vars(argument_parser.parse_args())
