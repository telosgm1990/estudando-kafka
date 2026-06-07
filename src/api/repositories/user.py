"""
References:

1. https://www.geeksforgeeks.org/python/how-to-hash-passwords-in-python/

"""

# Imports

from datetime import datetime, timedelta
from uuid import uuid4

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from src.common.database.client import DatabaseClient
from src.common.database.models.user import UserModel

# Objetos globais

_password_hasher = PasswordHasher()

# Funções


def _hash_password(raw_password: str) -> str:
    return _password_hasher.hash(raw_password)


def _verify_password(raw_password: str, hashed_password: str) -> bool:
    try:
        _password_hasher.verify(hashed_password, raw_password)
        return True

    except VerifyMismatchError:
        return False


def _generate_auth_token() -> str:
    return str(uuid4())


# Classes


class UsersRepository:
    """
    Repositório de usuários.
    """

    _database_client: DatabaseClient

    def __init__(self, database_client: DatabaseClient) -> None:
        self._database_client = database_client

    def does_user_exists(self, username: str) -> bool:
        """
        Verifica se um usuário existe.
        """

        user = self._get_user_by_username(username)
        return user is not None

    def does_user_password_match(
        self, username: str, raw_password: str
    ) -> bool:
        """
        Verifica se a senha do usuário confere.
        """

        user = self._get_user_by_username(username)
        if not user:
            raise Exception("user does not exist")

        entry_key, entry = user

        return _verify_password(raw_password, entry.hashed_password)

    def refresh_user_token(self, username: str) -> str:
        """
        Gera um novo token de autenticação para o usuário.
        """

        user = self._get_user_by_username(username)
        if not user:
            raise Exception("user does not exist")

        now = datetime.now()
        entry_key, entry = user
        entry.token = _generate_auth_token()
        entry.token_expires_at = now + timedelta(hours=1)
        entry.updated_at = now
        self._update_user_entry(entry_key, entry)

        return entry.token

    def register_new_user(self, username: str, raw_password: str) -> None:
        """
        Registra um novo usuário.
        """

        user = self._get_user_by_username(username)
        if user:
            raise Exception("user already exits")

        entry = UserModel(
            username=username,
            hashed_password=_hash_password(raw_password),
            created_at=datetime.now(),
        )
        self._add_user_entry(entry)

    def _get_user_by_username(
        self, username: str
    ) -> tuple[str, UserModel] | None:
        entries = self._get_user_entries()
        for entry_key, entry in entries.items():
            if entry.username.upper() == username.upper():
                return entry_key, entry

        return None

    def _get_user_entries(self) -> dict[str, UserModel]:
        return self._database_client.get_entries_from("users")

    def _update_user_entry(self, entry_key: str, entry: UserModel) -> None:
        updated_entries = {entry_key: entry}
        self._database_client.update_entries_into("users", updated_entries)

    def _add_user_entry(self, entry: UserModel) -> str:
        return self._database_client.add_entry_to("users", entry)
