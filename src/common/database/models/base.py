# Imports

import json

from pydantic import BaseModel as PydanticBaseModel

# Class


class DatabaseModel(PydanticBaseModel):
    """
    Classe base para modelos do banco.
    """

    @classmethod
    def from_json(cls, json_str: str) -> "DatabaseModel":
        """
        Desserializa o objeto de uma string JSON.
        """

        kwargs = json.loads(json_str)
        return cls(**kwargs)

    def to_json(self) -> str:
        """
        Serializa o objeto em formato JSON.
        """

        return self.model_dump_json()
