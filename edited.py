import numpy as np
from skimage import io, img_as_float, color
from scipy.ndimage import uniform_filter

def local_entropy(image, window_size=5, bins=64):
    """Compute local entropy map using histogram-based approximation."""
    # Quantize to bins
    quantized = np.floor(image * (bins - 1)).astype(np.int32)
    h, w = image.shape
    entropy_map = np.zeros_like(image)

    # Build binary masks for each bin and smooth them to estimate p(i)
    for b in range(bins):
        mask = (quantized == b).astype(np.float32)
        p = uniform_filter(mask, size=window_size)
        nonzero = p > 0
        entropy_map[nonzero] -= p[nonzero] * np.log2(p[nonzero])

    return entropy_map

def kuwahara_entropy_vectorized(image, window_size=5, bins=64):
    """Fully vectorized Kuwahara filter using entropy instead of variance."""
    if image.ndim == 3:
        # Process per channel
        return np.stack(
            [kuwahara_entropy_vectorized(image[..., c], window_size, bins) for c in range(image.shape[2])],
            axis=-1
        )

    pad = window_size // 2
    h, w = image.shape

    # Compute quadrant means (using uniform filters on subregions)
    mean_tl = uniform_filter(image, window_size)[pad:, pad:]  # top-left
    mean_tr = uniform_filter(image[:, ::-1], window_size)[pad:, pad:][:, ::-1]  # top-right
    mean_bl = uniform_filter(image[::-1, :], window_size)[pad:, pad:][::-1, :]  # bottom-left
    mean_br = uniform_filter(image[::-1, ::-1], window_size)[pad:, pad:][::-1, ::-1]  # bottom-right

    # Resize to match original
    mean_tl, mean_tr, mean_bl, mean_br = [
        m[:h, :w] for m in (mean_tl, mean_tr, mean_bl, mean_br)
    ]

    # Compute entropy maps for same quadrants
    ent_tl = local_entropy(image, window_size, bins)[pad:, pad:]
    ent_tr = local_entropy(image[:, ::-1], window_size, bins)[pad:, pad:][:, ::-1]
    ent_bl = local_entropy(image[::-1, :], window_size, bins)[pad:, pad:][::-1, :]
    ent_br = local_entropy(image[::-1, ::-1], window_size, bins)[pad:, pad:][::-1, ::-1]

    ent_tl, ent_tr, ent_bl, ent_br = [
        e[:h, :w] for e in (ent_tl, ent_tr, ent_bl, ent_br)
    ]

    # Stack and select best quadrant
    entropies = np.stack([ent_tl, ent_tr, ent_bl, ent_br], axis=-1)
    means = np.stack([mean_tl, mean_tr, mean_bl, mean_br], axis=-1)

    best_idx = np.argmin(entropies, axis=-1)
    output = np.take_along_axis(means, best_idx[..., None], axis=-1).squeeze(-1)

    return output

# Example usage:
if __name__ == "__main__":
    img = img_as_float(io.imread("images.jpeg"))
    if img.ndim == 2:
        gray = img
    else:
        gray = color.rgb2gray(img)
    
    # Entropy-based Kuwahara for color
    filtered_color = kuwahara_entropy_vectorized(img, window_size=5)
    io.imsave("kuwahara_entropy_color.jpg", (np.clip(filtered_color, 0, 1) * 255).astype(np.uint8))

    # Optional: grayscale
    filtered_gray = kuwahara_entropy_vectorized(gray, window_size=5)
    io.imsave("kuwahara_entropy_gray.jpg", (np.clip(filtered_gray, 0, 1) * 255).astype(np.uint8))
