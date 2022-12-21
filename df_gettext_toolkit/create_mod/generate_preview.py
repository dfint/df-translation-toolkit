import os
from pathlib import Path
from platform import system
from typing import Optional

import typer
from loguru import logger
from PIL import Image, ImageDraw, ImageFont


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    font_path: Path,
    font_size: int,
    color: tuple[int, int, int],
    shadow_color: Optional[tuple[int, int, int]] = None,
) -> None:
    font = ImageFont.truetype(font=str(font_path), size=font_size)
    if shadow_color:
        draw.multiline_text(
            xy=(xy[0] + 2, xy[1] + 1),
            text=text.replace("\\n", "\n"),
            font=font,
            align="center",
            fill=shadow_color,
            anchor="mm",
        )
    draw.multiline_text(
        xy=xy,
        text=text.replace("\\n", "\n"),
        font=font,
        align="center",
        fill=color,
        anchor="mm",
    )


possible_fonts = [
    "Candarab.ttf",
    "Candara.ttf",
    "FiraCode-Bold.ttf",
    "FiraCode-Regular.ttf",
    "FiraCode.ttf",
    "CascadiaMono.ttf",
    "bahnschrift.ttf" "Ubuntu-B.ttf",
    "Ubuntu-R.ttf",
    "Ubuntu.ttf",
    "verdanab.ttf",
    "verdana.ttf",
    "arialbd.ttf",
    "arial.ttf",
]


def default_font() -> Path:
    search_target: Path
    if system() == "Windows":
        search_target = Path(str(os.getenv("WINDIR")), "Fonts")
    else:
        search_target = Path("/usr/share/fonts/truetype")
    for font_name in possible_fonts:
        for font in search_target.glob(f"**/{font_name}"):
            return font
    raise Exception("Unable to find default font variant, pass font_path instead using default.")


def main(
    png_path: Path,
    title: str,
    subtitle: str,
    font_path: Optional[Path] = None,
    font_title_size: int = 195,
    font_subtitle_size: int = 85,
    title_y: float = 0.35,
    subtitle_y: float = 0.75,
    canvas_size: tuple[int, int] = (500, 500),
    background_color: tuple[int, int, int] = (0, 48, 73),
    main_color: tuple[int, int, int] = (252, 191, 73),
    second_color: Optional[tuple[int, int, int]] = (214, 40, 40),
    box_width: int = 10,
) -> None:
    assert png_path.parent.exists() and png_path.suffix == ".png", "Invalid png_path to output png image file"
    assert title_y < 1 and title_y > 0 and subtitle_y < 1 and subtitle_y > 0, "Invalid Y value, should be 0 < Y < 1"

    if not font_path:
        logger.info("Searching for default font")
        font_path = default_font()
        logger.info(f"Found {font_path.name}")

    img = Image.new("RGB", canvas_size, color=background_color)
    draw = ImageDraw.Draw(img)

    # Draw box
    if box_width > 0:
        if second_color:
            draw.rectangle(xy=(0, 0, *canvas_size), outline=second_color, width=box_width)
        draw.rectangle(xy=(0, 0, *canvas_size), outline=main_color, width=box_width - 2)

    # Draw Title
    draw_text(
        draw=draw,
        xy=(canvas_size[0] * 0.5, canvas_size[0] * title_y),
        text=title,
        font_path=font_path,
        font_size=font_title_size,
        color=main_color,
        shadow_color=second_color,
    )

    # Draw Subtitle
    draw_text(
        draw=draw,
        xy=(canvas_size[0] * 0.5, canvas_size[0] * subtitle_y),
        text=subtitle,
        font_path=font_path,
        font_size=font_subtitle_size,
        color=main_color,
        shadow_color=second_color,
    )

    img.save(png_path)
    logger.info("Preview generadet successfully")


if __name__ == "__main__":
    typer.run(main)
