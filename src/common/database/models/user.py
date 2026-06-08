# Imports

from datetime import datetime

from src.common.database.models.base import DatabaseModel

# Classes


class UserModel(DatabaseModel):
    """
    Modelo para entradas em .data/users.json
    """

    username: str
    hashed_password: str
    created_at: datetime
    token: str | None = None
    token_expires_at: datetime | None = None
    updated_at: datetime | None = None
