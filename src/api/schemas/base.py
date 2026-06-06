# Imports

from pydantic import BaseModel as PydanticBaseModel

# Classes


class ApiMessageResponse(PydanticBaseModel):
    """
    Schema para respostas da API do tipo mensagem.
    """

    message: str
