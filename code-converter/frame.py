from PIL import Image
from pathlib import Path
from loader import load_assets, BACKGROUND_PATH, FRAME_PATH, ARTWORK_PATH

EDGE_SLICE = 40  # Frame slice thickness in pixels
CURRENT_DIR = Path(__file__).parent
OUTPUT_PATH = CURRENT_DIR / "output.png"

def slice_frame_edges(frame_img, edge_width):
    w, h = frame_img.size

    # Extract corners
    top_left     = frame_img.crop((0, 0, edge_width, edge_width))
    top_right    = frame_img.crop((w - edge_width, 0, w, edge_width))
    bottom_left  = frame_img.crop((0, h - edge_width, edge_width, h))
    bottom_right = frame_img.crop((w - edge_width, h - edge_width, w, h))

    # Extract edges
    top_edge    = frame_img.crop((edge_width, 0, w - edge_width, edge_width))
    bottom_edge = frame_img.crop((edge_width, h - edge_width, w - edge_width, h))
    left_edge   = frame_img.crop((0, edge_width, edge_width, h - edge_width))
    right_edge  = frame_img.crop((w - edge_width, edge_width, w, h - edge_width))

    return {
        "top_left": top_left,
        "top_edge": top_edge,
        "top_right": top_right,
        "right_edge": right_edge,
        "bottom_right": bottom_right,
        "bottom_edge": bottom_edge,
        "bottom_left": bottom_left,
        "left_edge": left_edge
    }

def build_frame(artwork_size, frame_parts, edge_width):
    art_w, art_h = artwork_size
    new_w = art_w + 2 * edge_width
    new_h = art_h + 2 * edge_width

    result = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))

    # Place corners
    result.paste(frame_parts["top_left"], (0, 0))
    result.paste(frame_parts["top_right"], (new_w - edge_width, 0))
    result.paste(frame_parts["bottom_left"], (0, new_h - edge_width))
    result.paste(frame_parts["bottom_right"], (new_w - edge_width, new_h - edge_width))

    # Place top and bottom edges
    for x in range(edge_width, new_w - edge_width, frame_parts["top_edge"].width):
        result.paste(frame_parts["top_edge"], (x, 0))
        result.paste(frame_parts["bottom_edge"], (x, new_h - edge_width))

    # Place left and right edges
    for y in range(edge_width, new_h - edge_width, frame_parts["left_edge"].height):
        result.paste(frame_parts["left_edge"], (0, y))
        result.paste(frame_parts["right_edge"], (new_w - edge_width, y))

    return result

# Load assets
assets = load_assets(
    background_path=BACKGROUND_PATH,
    frame_path=FRAME_PATH,
    artwork_path=ARTWORK_PATH
)

# Generate frame and save
frame_parts = slice_frame_edges(assets["frame"], EDGE_SLICE)
dynamic_frame = build_frame(assets["artwork"].size, frame_parts, EDGE_SLICE)

# Save output
dynamic_frame.convert("RGB").save(OUTPUT_PATH)
print(f"[OK] Frame image saved to {OUTPUT_PATH}")
