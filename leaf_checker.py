"""
LEAF CHECKER v2 — Fixed for real-world photos
Much more lenient — rejects humans/objects but accepts real leaves
"""
import numpy as np
from PIL import Image
import cv2

def is_leaf(image, confidence_threshold=0.18):
    img = image.convert("RGB")
    img_np = np.array(img)

    img_hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
    h = img_hsv[:, :, 0]
    s = img_hsv[:, :, 1]
    v = img_hsv[:, :, 2]

    # Green (healthy leaves)
    green_mask = ((h >= 20) & (h <= 95) & (s >= 25) & (v >= 25))
    green_ratio = green_mask.mean()

    # Yellow/brown (diseased leaves)
    disease_mask = ((h >= 8) & (h <= 35) & (s >= 40) & (v >= 40))
    disease_ratio = disease_mask.mean()

    # Dark brown (severely diseased)
    dark_mask = ((h >= 5) & (h <= 25) & (s >= 20) & (v >= 15) & (v <= 120))
    dark_ratio = dark_mask.mean()

    # Texture (leaves have edges)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    texture = min(lap_var / 1000.0, 1.0)

    # Skin detection
    skin_mask = ((h >= 0) & (h <= 18) & (s >= 30) & (s <= 170) & (v >= 100))
    skin_ratio = skin_mask.mean()

    # Combine score
    leaf_score = (
        green_ratio   * 0.45 +
        disease_ratio * 0.20 +
        dark_ratio    * 0.10 +
        texture       * 0.25
    ) - (skin_ratio * 0.50)

    leaf_score = float(np.clip(leaf_score, 0, 1))

    if leaf_score >= confidence_threshold:
        return True, leaf_score, f"Leaf detected (score: {leaf_score:.2f})"

    # Build rejection reason
    if skin_ratio > 0.25:
        reason = "Human skin detected — please upload a tomato leaf image."
    elif green_ratio < 0.03 and disease_ratio < 0.05 and dark_ratio < 0.05:
        reason = "No plant colors found — please upload a tomato leaf image."
    else:
        reason = f"Not clearly a leaf (score: {leaf_score:.2f}) — try a clearer photo with better lighting."

    return False, leaf_score, reason