import cv2
import numpy as np

def median_kuwahara(img, window=5):
    """
    Kuwahara filter variant that uses the median instead of the mean
    for the least-variant subregion.
    """
    img = img.astype(np.float32)
    if img.ndim == 2:  # grayscale handling
        img = img[..., None]
    h, w, c = img.shape

    pad = window // 2
    padded = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_REFLECT)
    output = np.zeros_like(img, dtype=np.float32)

    for y in range(pad, h + pad):
        for x in range(pad, w + pad):
            region = padded[y - pad:y + pad + 1, x - pad:x + pad + 1]

            # 4 quadrants
            q1 = region[:pad + 1, :pad + 1]
            q2 = region[:pad + 1, pad:]
            q3 = region[pad:, :pad + 1]
            q4 = region[pad:, pad:]
            quadrants = [q1, q2, q3, q4]

            # compute variance and median per quadrant
            variances = [np.var(q, axis=(0, 1)).mean() for q in quadrants]
            medians = [np.median(q.reshape(-1, c), axis=0) for q in quadrants]

            # choose median of quadrant with smallest variance
            best_q = np.argmin(variances)
            output[y - pad, x - pad] = medians[best_q]

    output = np.clip(output, 0, 255)
    if c == 1:
        output = output[..., 0]
    return output.astype(np.uint8)


# Example usage
if __name__ == "__main__":
    img = cv2.imread("./images/a.jpg")
    out = median_kuwahara(img, window=7)
    cv2.imwrite("median_kuwahara_output.png", out)
    cv2.imshow("Median Kuwahara", out)
    cv2.waitKey(0)
