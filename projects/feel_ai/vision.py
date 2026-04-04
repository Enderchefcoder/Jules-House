import cv2
import numpy as np
import os

def vision_to_tokens(image_path, grid_size=(4, 4)):
    """
    Converts an image into structural and color tensors (Hex-encoded strings)
    to represent the 'energy' of the visual for an LLM to 'feel'.
    """
    if not os.path.exists(image_path):
        return f"Error: File {image_path} not found."

    # 1. Load image and convert to RGB
    img = cv2.imread(image_path)
    if img is None:
        return "Error: Could not decode image."
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 2. Divide into a grid to capture spatial "feeling"
    h, w, _ = img.shape
    gh, gw = h // grid_size[0], w // grid_size[1]

    sensory_blocks = []

    for r in range(grid_size[0]):
        for c in range(grid_size[1]):
            # Extract the grid cell
            cell = img[r*gh:(r+1)*gh, c*gw:(c+1)*gw]

            if cell.size == 0:
                continue

            # Calculate Average Color (RGB) and Brightness (Luminance)
            avg_color = np.mean(cell, axis=(0, 1)).astype(int)
            brightness = int(0.299*avg_color[0] + 0.587*avg_color[1] + 0.114*avg_color[2])

            # Convert to Hex Tokens: v[Row][Col]_[HexColor]_[BrightnessHex]
            hex_color = '{:02x}{:02x}{:02x}'.format(*avg_color)
            token = f"v{r}{c}_{hex_color}_{brightness:02x}"
            sensory_blocks.append(token)

    return f"<|VISUAL_SENSE: {'|'.join(sensory_blocks)} |>"

if __name__ == "__main__":
    # Test with a visual from the simulation
    test_img = "visual/aether_3d_v1.png"
    if os.path.exists(test_img):
        print(f"Feeling {test_img}...")
        print(vision_to_tokens(test_img))
    else:
        print(f"Sample image {test_img} not found for testing.")
