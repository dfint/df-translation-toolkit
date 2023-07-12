from pathlib import Path

import jinja2
import typer

# from cairosvg import svg2png


def generate_preview(template_text: str, title: str, description: str, destination_path: Path):
    template = jinja2.Template(template_text)
    result_svg = template.render(title=title, description=description)
    # svg2png(bytestring=result_svg, write_to=str(destination_path))
    with open(destination_path, "w") as preview:
        preview.write(result_svg)


def main(template_path: Path, title: str, description: str, destination_path: Path):
    with open(template_path) as template_file:
        template = template_file.read()
        generate_preview(template, title, description, destination_path)


if __name__ == "__main__":
    typer.run(main)
