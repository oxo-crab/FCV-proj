# app.py

import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import os
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

class ImageFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Filter Workbench")
        self.root.geometry("1200x800")

        # --- Image Storage ---
        self.original_image = None
        self.processed_image = None
        self.image_path = None

        # --- GUI Layout ---
        control_frame = tk.Frame(root, pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        image_frame = tk.Frame(root, padx=10, pady=10)
        image_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        # --- Image Canvases ---
        self.canvas_original = tk.Canvas(image_frame, bg="#2c3e50")
        self.canvas_original.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        tk.Label(self.canvas_original, text="Original Image", bg="#2c3e50", fg="white").place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.canvas_processed = tk.Canvas(image_frame, bg="#2c3e50")
        self.canvas_processed.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5)
        tk.Label(self.canvas_processed, text="Processed Image", bg="#2c3e50", fg="white").place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # --- Controls ---
        btn_load = tk.Button(control_frame, text="Load Image", command=self.load_image)
        btn_load.pack(side=tk.LEFT, padx=10)

        self.filter_options = [
            "Guided Filter",
            "Rolling Guidance Filter",
            "Kuwahara Filter",
            "Portrait - Standard Blur",
            "Portrait - Artistic Style"
        ]
        self.selected_filter = tk.StringVar(value=self.filter_options[0])
        filter_menu = ttk.Combobox(control_frame, textvariable=self.selected_filter, values=self.filter_options, state="readonly", width=25)
        filter_menu.pack(side=tk.LEFT, padx=10)

        # --- NEW --- Bind the on_filter_change function to the combobox selection event
        filter_menu.bind("<<ComboboxSelected>>", self.on_filter_change)

        btn_apply = tk.Button(control_frame, text="Apply Filter", command=self.apply_filter)
        btn_apply.pack(side=tk.LEFT, padx=10)

        # --- Metrics Display ---
        metrics_frame = tk.Frame(control_frame)
        metrics_frame.pack(side=tk.LEFT, padx=20)
        
        self.psnr_label = tk.Label(metrics_frame, text="PSNR: --", font=("Arial", 10))
        self.psnr_label.pack(side=tk.TOP)
        
        self.ssim_label = tk.Label(metrics_frame, text="SSIM: --", font=("Arial", 10))
        self.ssim_label.pack(side=tk.TOP)
    
    # --- NEW --- This function is called when a new filter is selected from the dropdown
    def on_filter_change(self, event=None):
        """Clears the processed image canvas when the filter selection changes."""
        if self.original_image is None:
            return # Do nothing if no image is loaded
            
        print(f"\nFilter selection changed to '{self.selected_filter.get()}'. Clearing view.")
        
        # Black out the canvas
        self.canvas_processed.delete("all")
        tk.Label(self.canvas_processed, text="Click 'Apply Filter' to see result", bg="#2c3e50", fg="white", font=("Arial", 12)).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Reset the metrics and the stored processed image
        self.processed_image = None
        self._calculate_and_display_metrics()

    def load_image(self):
        """Loads an image from file and displays it."""
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if not self.image_path:
            print("Image loading cancelled.")
            return

        print(f"Loading image from: {os.path.basename(self.image_path)}")
        self.original_image = cv2.imread(self.image_path)
        self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        print("Image loaded and converted to RGB successfully.")

        self.root.after(100, lambda: self.display_image(self.original_image, self.canvas_original))
        self.canvas_processed.delete("all")
        tk.Label(self.canvas_processed, text="Processed Image", bg="#2c3e50", fg="white").place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self._calculate_and_display_metrics() # Reset metrics on new image load

    def display_image(self, image_data, canvas):
        """Resizes and displays an image on the given canvas."""
        canvas.delete("all")
        img_height, img_width, _ = image_data.shape
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(100, lambda: self.display_image(image_data, canvas))
            return

        scale = min(canvas_width / img_width, canvas_height / img_height)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        if new_width > 0 and new_height > 0:
            resized_image = cv2.resize(image_data, (new_width, new_height))
            photo = ImageTk.PhotoImage(image=Image.fromarray(resized_image))
            canvas.create_image(canvas_width / 2, canvas_height / 2, image=photo, anchor=tk.CENTER)
            canvas.image = photo

    def apply_filter(self):
        """Applies the selected filter to the original image."""
        if self.original_image is None:
            print("Error: Please load an image first.")
            return

        choice = self.selected_filter.get()
        print(f"\nApplying filter: '{choice}'...")

        if choice == "Guided Filter":
            self.processed_image = self._guided_filter(self.original_image)
        elif choice == "Rolling Guidance Filter":
            self.processed_image = self._rolling_guidance_filter(self.original_image)
        elif choice == "Kuwahara Filter":
            self.processed_image = self._kuwahara_filter_vectorized(self.original_image)
        elif choice == "Portrait - Standard Blur":
            self.processed_image = self._create_portrait_effect(self.original_image, lambda img: cv2.GaussianBlur(img, (21, 21), 0))
        elif choice == "Portrait - Artistic Style":
            self.processed_image = self._create_portrait_effect(self.original_image, self._kuwahara_filter_vectorized)

        if self.processed_image is not None:
            print(f"'{choice}' filter applied successfully. Displaying result.")
            self.display_image(self.processed_image, self.canvas_processed)
            self._calculate_and_display_metrics()
        else:
            print(f"Filter '{choice}' failed to produce an output.")

    def _calculate_and_display_metrics(self):
        """Calculates PSNR and SSIM and updates the GUI labels."""
        if self.original_image is None or self.processed_image is None:
            self.psnr_label.config(text="PSNR: --")
            self.ssim_label.config(text="SSIM: --")
            return

        h, w, _ = self.original_image.shape
        processed_resized = cv2.resize(self.processed_image, (w, h))

        psnr_value = psnr(self.original_image, processed_resized, data_range=255)
        ssim_value = ssim(self.original_image, processed_resized, multichannel=True, data_range=255, channel_axis=2)

        self.psnr_label.config(text=f"PSNR: {psnr_value:.2f} dB")
        self.ssim_label.config(text=f"SSIM: {ssim_value:.4f}")
        print(f"Metrics Calculated -> PSNR: {psnr_value:.2f} dB, SSIM: {ssim_value:.4f}")

    # --- Filter Implementations ---

    def _guided_filter(self, image):
        return cv2.ximgproc.guidedFilter(guide=image, src=image, radius=10, eps=4000)

    def _rolling_guidance_filter(self, image):
        return cv2.ximgproc.rollingGuidanceFilter(image, sigmaSpace=10, sigmaColor=30, numOfIter=4)
        
    def _kuwahara_filter_vectorized(self, image, kernel_size=11):
        """Applies a fast, vectorized Kuwahara filter using OpenCV's built-in functions."""
        img_float = image.astype(np.float32)
        img_sq_float = img_float**2
        
        radius = (kernel_size - 1) // 2
        q_kernel_size = (radius + 1, radius + 1)
        
        anchors = [(radius, radius), (0, radius), (radius, 0), (0, 0)]
        means, sq_means = [], []

        for anchor in anchors:
            mean = cv2.boxFilter(img_float, -1, q_kernel_size, anchor=anchor, normalize=True, borderType=cv2.BORDER_REFLECT)
            sq_mean = cv2.boxFilter(img_sq_float, -1, q_kernel_size, anchor=anchor, normalize=True, borderType=cv2.BORDER_REFLECT)
            means.append(mean)
            sq_means.append(sq_mean)

        means = np.stack(means, axis=0)
        sq_means = np.stack(sq_means, axis=0)

        variances = sq_means - means**2
        intensity_variances = np.sum(variances, axis=3)
        min_variance_indices = np.argmin(intensity_variances, axis=0)

        h, w, _ = image.shape
        row_indices, col_indices = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')
        
        chosen_means = means[min_variance_indices, row_indices, col_indices]
        return chosen_means.astype(np.uint8)

    def _create_portrait_effect(self, image, background_filter_func):
        """Creates a portrait effect by segmenting the foreground."""
        print("  - Starting foreground segmentation (GrabCut)...")
        height, width, _ = image.shape
        rect = (int(width * 0.1), int(height * 0.1), int(width * 0.8), int(height * 0.8))

        mask = np.zeros(image.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        print("  - Segmentation complete.")

        foreground_mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        
        print("  - Processing background...")
        processed_background = background_filter_func(image)
        print("  - Background processing complete.")

        foreground = cv2.bitwise_and(image, image, mask=foreground_mask)
        background = cv2.bitwise_and(processed_background, processed_background, mask=1 - foreground_mask)

        return cv2.add(foreground, background)

# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageFilterApp(root)
    root.mainloop()