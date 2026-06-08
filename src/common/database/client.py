# Imports

import json
from pathlib import Path
from typing import Final
from uuid import uuid4

from src.common.settings import Settings

from src.common.database.models.base import DatabaseModel
from src.common.database.models.user import UserModel

# Constantes

_TABLES: Final[dict[str, type[DatabaseModel]]] = {
    "users": UserModel,
}

# Classes


class DatabaseClient:
    """
    Cliente para o banco de dados.
    """

    _data_directory_path: Path

    def __init__(self, settings: Settings) -> None:
        self._data_directory_path = settings.data_directory_path

    def get_entries_from(self, table_name: str) -> dict[str, DatabaseModel]:
        """
        Lista entradas de uma dada tabela
        """

        return self._get_entries_from(table_name)

    def add_entry_to(self, table_name: str, entry: DatabaseModel) -> str:
        """
        Adiciona uma nova entrada à uma data tabela.
        """

        entries = self._get_entries_from(table_name)

        entry_key = self._generate_new_entry_key(entries)
        entries[entry_key] = entry
        self._set_entries_into(table_name, entries)

        return entry_key

    def update_entries_into(
        self, table_name: str, updated_entries: dict[str, DatabaseModel]
    ) -> None:
        """
        Atualiza as entreadas
        """

        entries = self._get_entries_from(table_name)
        if any(entry_key not in entries for entry_key in updated_entries):
            raise Exception("some entries do not exist on table")

        entries.update(updated_entries)
        self._set_entries_into(table_name, entries)

    def _get_entries_from(self, table_name: str) -> dict[str, DatabaseModel]:
        file_path = self._get_table_file_path(table_name)
        if not file_path.exists():
            return dict()

        with open(file_path) as file:
            content = file.read() or "{}"

        entries_dict = json.loads(content)
        model_class = _TABLES[table_name]

        return {
            entry_key: model_class.from_json(entry_json)
            for entry_key, entry_json in entries_dict.items()
        }

    def _set_entries_into(
        self, table_name: str, entries: dict[str, DatabaseModel]
    ) -> None:
        entries_dict = {
            entry_key: entry.to_json() for entry_key, entry in entries.items()
        }
        file_path = self._get_table_file_path(table_name)

        with open(file_path, "w") as file:
            file.write(json.dumps(entries_dict, indent=4))

    def _generate_new_entry_key(
        self, entries: dict[str, DatabaseModel]
    ) -> str:
        entry_keys = set(entries.keys())

        new_entry_key = str(uuid4())
        while new_entry_key in entry_keys:
            new_entry_key = str(uuid4())

        return new_entry_key

    def _get_table_file_path(self, table_name: str) -> Path:
        file_name = f"{table_name}.json"
        return self._data_directory_path.joinpath(file_name)
