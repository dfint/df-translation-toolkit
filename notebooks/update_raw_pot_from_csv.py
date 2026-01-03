import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from pathlib import Path

    from babel.messages.pofile import read_po, write_po

    from df_translation_toolkit.parse.parse_raws import is_translatable, join_tag, split_tag
    from df_translation_toolkit.utils.csv_utils import read_csv

    return (
        Path,
        is_translatable,
        join_tag,
        read_csv,
        read_po,
        split_tag,
        write_po,
    )


@app.cell
def _(Path, read_csv):
    csv_data = read_csv(Path("../../vietnamese.csv"), encoding="utf-8")
    dictionary = {text: translation for text, translation, *_ in csv_data}
    dictionary
    return (dictionary,)


@app.cell
def _(read_po):
    with open("for_translation_dwarf-fortress-steam_objects_vi.po", "rb") as po_file:
        catalog = read_po(po_file)
    return (catalog,)


@app.cell
def _(catalog, dictionary, is_translatable, join_tag, split_tag):
    for message in catalog:
        if not message.id or message.string:
            continue

        parts = split_tag(message.id)
        translation_parts = []
        for part in parts:
            if not part or not is_translatable(part):
                translation_parts.append(part)
                continue

            translation = dictionary.get(part)
            if not translation:
                translation_parts = None
                break

            translation_parts.append(translation)

        if translation_parts:
            translation = join_tag(translation_parts)
            message.string = translation
    return


@app.cell
def _(catalog, write_po):
    with open("output.po", "wb") as output_po_file:
        write_po(catalog=catalog, fileobj=output_po_file)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
