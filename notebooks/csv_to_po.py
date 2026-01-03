import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from pathlib import Path

    from babel.messages import Catalog
    from babel.messages.pofile import write_po

    from df_translation_toolkit.utils.csv_utils import read_csv
    from df_translation_toolkit.utils.po_utils import default_header

    return Catalog, Path, default_header, read_csv, write_po


@app.cell
def _(Path, read_csv):
    csv_data = read_csv(Path("../../vietnamese.csv"), encoding="utf-8")
    return (csv_data,)


@app.cell
def _(Catalog, csv_data):
    catalog = Catalog()

    for text, translation in csv_data:
        if not isinstance(translation, str):
            translation = ""  # noqa: PLW2901
        catalog.add(id=text, string=translation)
    return (catalog,)


@app.cell
def _(catalog, default_header, write_po):
    with open("vietnamese.po", "wb") as po_file:
        po_file.write(default_header + b"\n\n")
        write_po(po_file, catalog, omit_header=True)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
