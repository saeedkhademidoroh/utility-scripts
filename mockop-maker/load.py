from PIL import Image
from pathlib import Path

# Get the directory of the current script
CURRENT_DIR = Path(__file__).parent

# Define image file paths relative to script location
BACKGROUND_PATH = CURRENT_DIR / "back.jpg"
FRAME_PATH = CURRENT_DIR / "frame.jpg"
ARTWORK_PATH = CURRENT_DIR / "art.jpg"

def load_image(path):
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    image = Image.open(path).convert("RGBA")
    return image

def load_assets(background_path, frame_path, artwork_path):
    background = load_image(background_path)
    frame = load_image(frame_path)
    artwork = load_image(artwork_path)

    return {
        "background": background,
        "frame": frame,
        "artwork": artwork
    }

# Load and preview assets
assets = load_assets(
    background_path=BACKGROUND_PATH,
    frame_path=FRAME_PATH,
    artwork_path=ARTWORK_PATH
)

assets["background"].show(title="Background")
assets["frame"].show(title="Frame")
assets["artwork"].show(title="Artwork")

for name, img in assets.items():
    print(f"{name}: {img.size}, {img.mode}")
