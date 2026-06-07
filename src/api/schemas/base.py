# Imports

from typing import Generic, TypeVar

from pydantic import BaseModel as PydanticBaseModel

# Tipos protegidos

_T = TypeVar("_T")


# Classes


class ApiDataResponse(PydanticBaseModel, Generic[_T]):
    """
    Schema para respostas da API do tipo dados.
    """

    data: _T


class ApiMessageResponse(PydanticBaseModel):
    """
    Schema para respostas da API do tipo mensagem.
    """

    message: str
