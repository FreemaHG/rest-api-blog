FROM python:3.11.5-slim

COPY requirements/base.txt /src/requirements/base.txt
COPY requirements/dev.txt /src/requirements/dev.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements/dev.txt

COPY ./migrations /migrations

COPY alembic.ini /alembic.ini

COPY ./src /src

COPY ./docker /docker

# Разрешаем Docker выполнять команды в ./docker/<file>.sh (bash-команды),
# используемые для загрузки демонстрационных данных и запуска сервера
RUN chmod a+x docker/*.sh