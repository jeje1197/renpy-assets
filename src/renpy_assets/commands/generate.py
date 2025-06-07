import re
from pathlib import Path
import typer
from src.renpy_assets.utils.file_utilities import find_files_by_patterns

app = typer.Typer(help="Generate RenPy asset declarations.")

# Asset regex patterns map
ASSET_TYPES = {
    "images": [r".*\.(png|jpg|jpeg|webp|bmp|gif)$"],
    "audio": [r".*\.(mp3|ogg|wav|m4a)$"],
    "fonts": [r".*\.(ttf|otf|woff|woff2)$"],
}


@app.command()
def generate(
    asset_type: str = typer.Argument(..., help="Asset type to generate declarations for (images, audio, fonts)"),
    path: Path = typer.Option(Path("game"), "--path", "-p", help="Base directory to scan for assets"),
    output: Path = typer.Option(None, "--output", "-o", help="Output .rpy file path (defaults to <path>/generated_assets.rpy)")
):
    """
    Generate RenPy asset declarations for a given asset type by scanning the project directory.
    """
    asset_type = asset_type.lower()
    if asset_type not in ASSET_TYPES:
        typer.echo(f"Unsupported asset type '{asset_type}'. Supported types: {', '.join(ASSET_TYPES.keys())}")
        raise typer.Exit(code=1)

    if not path.exists() or not path.is_dir():
        typer.echo(f"Specified path '{path}' does not exist or is not a directory.")
        raise typer.Exit(code=1)

    typer.echo(f"Scanning {asset_type} assets in {path}...")

    patterns = ASSET_TYPES[asset_type]
    files = find_files_by_patterns(str(path), patterns)

    if not files:
        typer.echo(f"No {asset_type} assets found in {path}.")
        raise typer.Exit()

    output_file = output or (path / "generated_assets.rpy")

    lines = [f"# Auto-generated RenPy {asset_type} declarations\n"]

    for file_path in sorted(files):
        name = normalize_name(file_path, path)
        relative_path = file_path.relative_to(path)
        line = generate_declaration_line(asset_type, name, relative_path)
        lines.append(line)

    content = "\n".join(lines) + "\n"

    output_file.write_text(content, encoding="utf-8")
    typer.echo(f"Wrote {len(files)} {asset_type} declarations to {output_file}")


def normalize_name(path: Path, root_dir: Path) -> str:
    """
    Create a valid RenPy identifier from the relative path.

    Example: "images/bg-menu.png" -> "bg_menu"

    Args:
        path (Path): The file path.
        root_dir (Path): Base directory to compute relative path.

    Returns:
        str: Normalized name string.
    """
    relative_path = path.relative_to(root_dir)
    # Use parts excluding file extension, replace non-alphanumeric with underscores
    name_parts = list(relative_path.with_suffix('').parts)
    name = "_".join(name_parts)
    # Replace invalid chars with underscore and lowercase
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name).lower()
    return name


def generate_declaration_line(asset_type: str, name: str, relative_path: Path) -> str:
    """
    Generate the RenPy declaration line depending on asset type.

    Args:
        asset_type (str): 'images', 'audio', or 'fonts'
        name (str): normalized asset name
        relative_path (Path): path relative to base directory

    Returns:
        str: RenPy declaration line
    """
    path_str = str(relative_path).replace("\\", "/")  # Use forward slashes for RenPy

    if asset_type == "images":
        return f'image {name} = "{path_str}"'
    elif asset_type == "audio":
        return f'define audio.{name} = "{path_str}"'
    elif asset_type == "fonts":
        return f'define font.{name} = "{path_str}"'
    else:
        return ""

