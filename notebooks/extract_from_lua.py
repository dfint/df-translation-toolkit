import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from df_translation_toolkit.parse.parse_lua import parse_lua_file
    from pathlib import Path
    import pandas as pd
    return Path, parse_lua_file, pd


@app.cell
def _(Path):
    game_path = Path("../game/df_53_08_win_s")
    lua_file_path = game_path / "data/vanilla/vanilla_procedural/scripts"
    return (lua_file_path,)


@app.cell
def _(lua_file_path):
    lua_files = list(file for file in lua_file_path.rglob("*.lua"))
    return (lua_files,)


@app.cell
def _(lua_files, parse_lua_file, pd):
    result = []
    for file_path in lua_files:
        with file_path.open(encoding="cp437") as file:
            for item in parse_lua_file(lines=file):
                if item.is_translatable:
                    result.append(item)

    dataframe = pd.DataFrame(result)
    dataframe
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
