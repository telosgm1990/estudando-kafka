# Imports

import os
from pathlib import Path
from typing import Final

# Constantes globais

PROJECT_ROOT_PATH: Final[Path] = Path(
    os.path.abspath(__file__)
).parent.parent.parent
DATA_PATH: Final[Path] = PROJECT_ROOT_PATH.joinpath(".data")
