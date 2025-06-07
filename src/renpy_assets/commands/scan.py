from pathlib import Path
import typer
from src.renpy_assets.utils.file_utilities import find_files_by_patterns

app = typer.Typer(help="Scan Ren'Py assets like images, audio, or fonts.")

ASSET_TYPES = {
    "images": [r"\.png$", r"\.jpg$", r"\.jpeg$", r"\.webp$"],
    "audio": [r"\.ogg$", r"\.mp3$", r"\.wav$"],
    "fonts": [r"\.ttf$", r"\.otf$"],
}

@app.command()
def scan(
    asset_type: str = typer.Argument(..., help="The asset type to scan (e.g., images, audio, fonts)."),
    path: Path = typer.Option("game", "--path", "-p", help="Directory to scan from")
):
    """
    Scan and report assets of a specified type in the Ren'Py project.

    Args:
        asset_type (str): The category of assets to scan.
            Supported values: "images", "audio", "fonts".
        path (Path): The base directory to begin the search. Defaults to "game".

    Usage:
        renpy-assets scan asset images --path assets/
    """
    if asset_type is None:
        typer.echo("Please provide an asset type to scan. Supported types: images, audio, fonts.")
        raise typer.Exit(code=1)

    if asset_type not in ASSET_TYPES:
        typer.echo(f"Unsupported asset type: '{asset_type}'. Use one of: {', '.join(ASSET_TYPES.keys())}.")
        raise typer.Exit(code=1)

    typer.echo(f"Scanning {asset_type} assets in {path.resolve()} ...")

    patterns = ASSET_TYPES[asset_type]
    results = find_files_by_patterns(str(path), patterns)

    if results:
        typer.echo(f"Found {len(results)} {asset_type} assets.")
        for file_path in results:
            typer.echo(str(file_path))
    else:
        typer.echo("No matching assets found.")
