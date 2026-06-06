# Recrie a venv

rm -r .dev.venv
py -m venv .dev.venv


# Instale as dependências Python de desenvolvimento

.\.dev.venv\Scripts\python.exe -m pip install -U pip
.\.dev.venv\Scripts\pip.exe install -e .[dev]
