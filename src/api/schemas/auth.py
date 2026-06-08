# Imports

from pydantic import BaseModel as PydanticBaseModel

from src.api.schemas.base import ApiDataResponse, ApiMessageResponse

# Classes


class LoginRequestBody(PydanticBaseModel):
    """
    Requisição do endpoint `POST /auth/login`
    """

    username: str
    password: str


class LoginResponseData(PydanticBaseModel):
    """
    Tipo experado para LoginResponseBody::data
    """

    token: str


class LoginResponseBody(ApiDataResponse[LoginResponseData]):
    """
    Resposta do endpoint `POST /auth/login`
    """


class RegisterUserRequestBody(PydanticBaseModel):
    """
    Requisição do endpoint `post /auth/register`
    """

    username: str
    password: str


class RegisterUserResponseBody(ApiMessageResponse):
    """
    Resposta do endpoint `POST /auth/register`
    """
