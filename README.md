# base-api

Base API project structure

## Initialization
- Create a virtual environment
```shell
python -m venv .venv
```
* Activate the virtual environment
    - Mac OS/Linux
    ```shell
    source .venv/bin/activate
    ```
    - Windows
    ```shell
    ./venv/Scripts/activate
    ```
## Run
- Development
```shell
fastapi dev
```

## Migrations
- Run migrations
```shell
alembic upgrade head
```
- Create migrations
```shell
alembic revision --autogenerate -m YOUR_MESSAGE_HERE
```

## Seed
To delete the current data, use `--clean` option.
```shell
python -m app.cmd seed [--clean]
```