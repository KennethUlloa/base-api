from asyncio import run
from app.seeds import run as run_seeds
from typer import Typer, Option, Argument

app = Typer()


@app.command(help="Run seeds")
def seed(
    clean: bool = Option(False, help="Clean database before seeding"),
    name: str = Argument("all", help="Name of seed to run"),
):
    run(run_seeds(clean, name))


@app.command(help="Run migrations")
def migrate():
    raise NotImplementedError


if __name__ == "__main__":
    app()
