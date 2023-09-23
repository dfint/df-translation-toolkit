import typer

from df_translation_toolkit.csv_bisect import csv_bisect

app = typer.Typer()
app.command(name="csv_bisect")(csv_bisect.main)
