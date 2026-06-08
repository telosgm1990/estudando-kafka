# Imports

from http import HTTPStatus

from fastapi import FastAPI
from loguru import logger

from src.api.repositories.user import UsersRepository
from src.api.schemas.auth import (
    RegisterUserResponseBody,
    RegisterUserRequestBody,
    LoginResponseData,
    LoginResponseBody,
)
from src.common.settings import Settings

# Funções


def add_auth_routes(
    app: FastAPI, settings: Settings, users_repo: UsersRepository
) -> None:
    """
    Adiciona rotas de autenticação: /auth
    """

    @app.post("/auth/register", status_code=HTTPStatus.CREATED)
    def register_user(
        request_body: RegisterUserRequestBody,
    ) -> RegisterUserResponseBody:
        """
        Registra um novo usuário na API.
        """

        logger.info("registering a new user")

        # Verifique se o usuário existe
        if users_repo.does_user_exists(request_body.username):
            raise Exception("username already exists")

        # Registre o usuário
        users_repo.register_new_user(
            request_body.username, request_body.password
        )

        # Monte a resposta
        return RegisterUserResponseBody(message="user registered successfully")

    @app.post("/auth/login", status_code=HTTPStatus.CREATED)
    def login(request_body: RegisterUserRequestBody) -> LoginResponseBody:
        """
        Autentica o usuário na API.
        """

        logger.info("logging user in")

        # Verifique se o usuário existe
        if not users_repo.does_user_exists(request_body.username):
            raise Exception("invalid username/password")

        # Verifique se a senha confere
        if not users_repo.does_user_password_match(
            request_body.username, request_body.password
        ):
            raise Exception("invalid username/password")

        # Gere um novo token
        new_token = users_repo.refresh_user_token(request_body.username)

        # Monte a resposta
        return LoginResponseBody(data=LoginResponseData(token=new_token))
