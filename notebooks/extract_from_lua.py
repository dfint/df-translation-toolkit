import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from pathlib import Path

    import pandas as pd

    from df_translation_toolkit.parse.parse_lua import parse_lua_file
    return Path, parse_lua_file, pd


@app.cell
def _(Path):
    current_dir = Path(__file__).parent
    game_path = current_dir / "../../game/df_53_08_win_s"
    lua_file_path = game_path / "data/vanilla/vanilla_procedural/scripts"
    return (lua_file_path,)


@app.cell
def _(lua_file_path, parse_lua_file, pd):
    result = []
    for file_path in lua_file_path.rglob("*.lua"):
        with file_path.open(encoding="cp437") as file:
            for item in parse_lua_file(lines=file):
                if item.is_translatable:
                    result.append(item)  # noqa: PERF401

    dataframe = pd.DataFrame(result)
    dataframe
    return (result,)


@app.cell
def _(result):
    from collections import defaultdict
    duplicates = defaultdict(set)
    for _item in result:
        duplicates[_item.text].add(_item.line.strip().rstrip(","))
    return (duplicates,)


@app.cell
def _(duplicates):
    sorted_duplicates = sorted(duplicates.items(), key=lambda x: -len(x[1]))
    for i, (key, value) in enumerate(sorted_duplicates):
        sorted_duplicates[i] = key, list(value)
    sorted_duplicates
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
