from pathlib import Path
from renpy_assets.commands.generate import normalize_name, generate_declaration_line

def test_normalize_name():
    root = Path("/project/game")
    path = Path("/project/game/images/bg-menu.png")
    name = normalize_name(path, root)
    assert name == "images_bg_menu"


def test_generate_declaration_line():
    rel_path = Path("images/bg_menu.png")
    line = generate_declaration_line("images", "bg_menu", rel_path)
    assert line == 'image bg_menu = "images/bg_menu.png"'

    line = generate_declaration_line("audio", "theme_song", Path("audio/theme.ogg"))
    assert line == 'define audio.theme_song = "audio/theme.ogg"'

    line = generate_declaration_line("fonts", "main_font", Path("fonts/arial.ttf"))
    assert line == 'define font.main_font = "fonts/arial.ttf"'
