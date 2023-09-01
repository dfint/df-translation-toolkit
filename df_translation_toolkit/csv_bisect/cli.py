import typer

from df_translation_toolkit.csv_bisect import csv_bisect

app = typer.Typer()
app.command(name="from_string_dump")(csv_bisect.main)
