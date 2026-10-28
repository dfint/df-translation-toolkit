import typer

from cli import convert, create_mod, create_pot, translate

app = typer.Typer()
app.add_typer(convert.app, name="convert")
app.add_typer(create_pot.app, name="create_pot")
app.add_typer(create_mod.app, name="create_mod")
app.add_typer(translate.app, name="translate")
