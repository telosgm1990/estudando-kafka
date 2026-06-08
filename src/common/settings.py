# Imports

import os
from pathlib import Path
from typing import Final, Literal
from typing_extensions import Self

from pydantic import model_validator
from pydantic_settings import BaseSettings

# Tipos

LogLevel = Literal["debug", "info"]

# Constantes globais

PROJECT_ROOT_PATH: Final[Path] = Path(
    os.path.abspath(__file__)
).parent.parent.parent


# Classes


class Settings(BaseSettings):
    """
    Configurações do projeto.
    """

    log_level: LogLevel = "info"
    log_directory: str = str(PROJECT_ROOT_PATH.joinpath(".logs"))
    data_directory: str = str(PROJECT_ROOT_PATH.joinpath(".data"))
    api_host: str = "127.0.0.1"
    api_port: int = 8037
    api_reload: bool = False

    @property
    def log_directory_path(self) -> Path:
        """
        Retorna um objeto Path para o diretório de logs.
        """

        return Path(self.log_directory).absolute()

    @property
    def data_directory_path(self) -> Path:
        """
        Retorna um objeto Path para o diretório de dados.
        """

        return Path(self.data_directory).absolute()

    @classmethod
    def from_env_file(cls, env_file: str) -> "Settings":
        """
        Constroi o objeto de configurações utilizando um arquivo .env
        """

        return cls(_env_file=env_file)

    def as_json(self) -> str:
        """
        Returna o objeto de configurações em formato string JSON.
        """

        return self.model_dump_json()

    @model_validator(mode="after")
    def _validate_paths(self) -> Self:
        for attr_name in ("log_directory", "data_directory"):
            directory_path = Path(getattr(self, attr_name))

            if not directory_path.is_dir():
                directory_path.mkdir(exist_ok=True)

        return self
