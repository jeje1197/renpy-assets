# renpy-assets

A command-line interface for automating asset management in Ren'Py visual novel projects.

Easily scan your project for images, audio, and font assets, and generate boilerplate declarations to speed up scripting in `.rpy` files.

---

## ✨ Features

### 🔍 Scan Assets

Identify all assets in your Ren'Py project based on type:

- **images** – `.png`, `.jpg`, `.jpeg`, `.webp`
- **audio** – `.ogg`, `.mp3`, `.wav`
- **fonts** – `.ttf`, `.otf`

You can also scan **all** asset types at once.

```bash
renpy-assets scan images --path assets/images
renpy-assets scan audio
renpy-assets scan all
```

This prints a nicely formatted list of found assets, organized by category.

---

### 🪄 Generate Declarations

Automatically generate Ren'Py declarations for your assets:

```bash
renpy-assets generate images --path game/images --output image_decls.rpy
renpy-assets generate fonts --path assets/fonts --output fonts.rpy
renpy-assets generate all --output assets.rpy
```

This creates `.rpy`-ready declarations such as:

```renpy
# --- Image Assets ---
image bg_room = "images/bg room.png"
image character_happy = "images/character happy.png"

# --- Audio Assets ---
define audio.button_click = "audio/ui/click.ogg"

# --- Font Assets ---
define inter_font = "fonts/Inter-Regular.ttf"
```

Output filenames and directories are customizable via the `--output` and `--path` flags.

---

## 📦 Installation

```bash
pip install renpy-assets
```

For local development:

```bash
git clone https://github.com/jeje1197/renpy-assets
cd renpy-assets
pip install -e .
```

---

## 📁 Project Layout

```
src/
  renpy_assets/
    cli.py
    commands/
      scan.py
      generate.py
    utils/
      file_utilities.py

tests/
```

---

## 🧪 Testing

Run all tests using:

```bash
pytest
```

Make sure you're in the root directory and `src` is on the Python path.

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to get involved.