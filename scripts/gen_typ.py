# Authors: GLM-4.7🧙‍♂️, scillidan🤡

import sys
import os
import subprocess


def escape_typst(text):
    return (
        text.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("#", "\\#")
        .replace("{", "\\{")
        .replace("}", "\\}")
    )


def format_size(size_value):
    """Convert string size to proper Typst format."""
    return size_value if size_value.endswith("%") else size_value


def get_base_name(filename):
    """Remove all extensions from filename."""
    return filename.split(".")[0]


def generate_typst(mode, image, text_first, text_second, text_third, start, resize, size):
    flipped = mode == "landscape"
    text_third_escaped = escape_typst(text_first)
    text_second_escaped = escape_typst(text_second)
    text_first_escaped = escape_typst(text_third)
    image_path = f"../{image}"

    return f'''#import "@preview/polario-frame:1.0.0": *

#let render-polario(params) = {{
  set page(fill: black, margin: 2%, flipped: params.flipped)
  set text(font: ("MonaspiceNe NFM", "Sarasa Mono SC"))
  let img = crop(bytes(read(params.img-path, encoding: none)), start: params.start, resize: params.resize)
  render(params.size, theme: params.theme, img: img, ext-info: params.ext-info)
}}

#let ext-info = (
  "background": rgb("#00000000"),
  "first": text(size: 11pt, fill: white)[
    {text_first_escaped}
  ],
  "second": text(size: 11pt, fill: white)[
    {text_second_escaped}
  ],
  "third": text(size: 11pt, fill: white)[
    _{text_third_escaped}_
  ],
)

#let params = (
  "ext-info": ext-info,
  "theme": "classic-bottom-three",
  "img-path": "{image_path}",
  "flipped": {"true" if flipped else "false"},
  "start": {start},
  "resize": {resize},
  "size": {size},
)

#render-polario(params)
'''


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(
            "Usage: python add.py <mode> <image> <text-first> <text-second> <text-third> <start> <resize> <size>",
            file=sys.stderr,
        )
        sys.exit(1)

    mode = sys.argv[1]
    image = sys.argv[2]
    text_first = sys.argv[3]
    text_second = sys.argv[4]
    text_third = sys.argv[5]
    start = sys.argv[6]
    resize = sys.argv[7]
    size = sys.argv[8]

    # Get base name without extension
    base_name = get_base_name(image)
    typst_content = generate_typst(mode, image, text_first, text_second, text_third, start, resize, size)

    os.makedirs("typs", exist_ok=True)
    os.makedirs("pdfs", exist_ok=True)
    os.makedirs("jpgs", exist_ok=True)

    # Generate Typst file with base name
    typst_filename = f"typs/{base_name}.typ"
    with open(typst_filename, "w", encoding="utf-8") as f:
        f.write(typst_content)

    # Compile to PDF
    pdf_filename = f"pdfs/{base_name}.pdf"
    subprocess.run(
        ["typst", "compile", "--root", ".", typst_filename, pdf_filename],
        check=True,
    )

    # Convert to JPG
    jpg_pattern = f"jpgs/{base_name}.jpg"
    subprocess.run(
        [
            "magick",
            "-density",
            "96",
            pdf_filename,
            "-background",
            "white",
            "-alpha",
            "remove",
            "-quality",
            "90",
            jpg_pattern,
        ],
        check=True,
    )

    print(f"Generated: {typst_filename}, {pdf_filename}")
