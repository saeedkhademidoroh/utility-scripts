# Import third-party libraries
from PIL import Image

# Import standard libraries
from pathlib import Path

# Get the directory of the current script
CURRENT_DIR = Path(__file__).parent

# Define image file paths relative to script location
BACKGROUND_PATH = CURRENT_DIR / "back.jpg"
FRAME_PATH = CURRENT_DIR / "frame.jpg"
ARTWORK_PATH = CURRENT_DIR / "art.jpg"

# Function to load an image with error handling
"""
Load an image from the given path and convert it to RGBA.

Args:
    path (Path): Path to the image file.

Returns:
    Image.Image: The loaded PIL image in RGBA mode.
"""
def load_image(path):
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    return Image.open(path).convert("RGBA")

# Function to load all required assets
"""
Load background, frame, and artwork images from given paths.

Args:
    background_path (Path): Path to the background image.
    frame_path (Path): Path to the frame image.
    artwork_path (Path): Path to the artwork image.

Returns:
    dict: Dictionary containing loaded PIL images.
"""
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

# Print confirmation message
print("\n✅ asset_loader.py successfully executed")
