# ml_impact_test.py
import numpy as np
import cv2
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

def kuwahara_filter(image, kernel_size=5):
    """A simplified Kuwahara filter for demonstration."""
    # Ensure image is uint8 as required by this OpenCV function
    if image.dtype != np.uint8:
        image = image.astype(np.uint8)
    # The Kuwahara function in ximgproc expects a BGR or Grayscale image, not RGB
    # Since our data is synthetic and single channel, this is fine.
    return cv2.ximgproc.kuwahara(image, cv2.ximgproc.KUWAHARA_GENERALIZED, kernel_size, kernel_size)

# 1. Create a synthetic dataset
print("1. Generating synthetic dataset...")
X, y = make_blobs(n_samples=500, centers=4, n_features=64, random_state=42, cluster_std=4.0)
X = np.abs(X)
X = (X / X.max() * 255).astype(np.uint8)
X_images = X.reshape(-1, 8, 8) # 500 images of 8x8 pixels

# 2. Baseline: Train K-NN on the original noisy data
print("\n2. Testing classifier on original, noisy data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
accuracy_original = accuracy_score(y_test, y_pred)
print(f"   => Accuracy on original data: {accuracy_original:.2%}")

# 3. Apply a smoothing filter to the images
print("\n3. Applying Kuwahara filter to the entire dataset...")
X_images_smoothed = np.array([kuwahara_filter(img) for img in X_images])

# 4. Train K-NN on the smoothed data
print("\n4. Testing classifier on smoothed data...")
X_smoothed = X_images_smoothed.reshape(-1, 64) # Flatten images back to feature vectors
X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(X_smoothed, y, test_size=0.3, random_state=42)
knn_smoothed = KNeighborsClassifier(n_neighbors=5)
knn_smoothed.fit(X_train_s, y_train_s)
y_pred_s = knn_smoothed.predict(X_test_s)
accuracy_smoothed = accuracy_score(y_test_s, y_pred_s)
print(f"   => Accuracy on smoothed data: {accuracy_smoothed:.2%}")

# 5. Conclusion
print("\n--- Conclusion ---")
improvement = accuracy_smoothed - accuracy_original
print(f"The smoothing filter changed the classification accuracy by {improvement:+.2%}.")
if improvement > 0:
    print("This demonstrates that smoothing can act as a beneficial pre-processing step by removing noise.")
else:
    print("In this case, smoothing did not improve (or worsened) performance, possibly by removing useful features.")