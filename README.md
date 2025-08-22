# base-api

Base API project structure

## Run
- Development
```
fastapi dev
```

## Migrations
- Run migrations
```
alembic upgrade head
```
- Create migrations
```
alembic revision --autogenerate -m YOUR_MESSAGE_HERE
```

## Seed
To delete the current data, use `--clean` option.
```
 python -m app.cmd seed [--clean]
```