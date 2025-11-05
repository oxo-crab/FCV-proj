# app.py

import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import os
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
from scipy.ndimage import uniform_filter

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
        # Left frame for original image
        left_frame = tk.Frame(image_frame)
        left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        tk.Label(left_frame, text="Original Image", bg="#34495e", fg="white", font=("Arial", 11, "bold"), pady=5).pack(side=tk.TOP, fill=tk.X)
        self.canvas_original = tk.Canvas(left_frame, bg="#2c3e50", highlightthickness=0)
        self.canvas_original.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        # Right frame for processed image
        right_frame = tk.Frame(image_frame)
        right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5)
        tk.Label(right_frame, text="Processed Image", bg="#34495e", fg="white", font=("Arial", 11, "bold"), pady=5).pack(side=tk.TOP, fill=tk.X)
        self.canvas_processed = tk.Canvas(right_frame, bg="#2c3e50", highlightthickness=0)
        self.canvas_processed.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        # --- Controls ---
        btn_load = tk.Button(control_frame, text="Load Image", command=self.load_image)
        btn_load.pack(side=tk.LEFT, padx=10)

        self.filter_options = [
            "Guided Filter",
            "Rolling Guidance Filter",
            "Kuwahara Filter",
            "Kuwahara Filter (Entropy-based)"
        ]
        self.selected_filter = tk.StringVar(value=self.filter_options[0])
        filter_menu = ttk.Combobox(control_frame, textvariable=self.selected_filter, values=self.filter_options, state="readonly", width=25)
        filter_menu.pack(side=tk.LEFT, padx=10)

        # --- NEW --- Bind the on_filter_change function to the combobox selection event
        filter_menu.bind("<<ComboboxSelected>>", self.on_filter_change)

        btn_apply = tk.Button(control_frame, text="Apply Filter", command=self.apply_filter)
        btn_apply.pack(side=tk.LEFT, padx=10)

        # --- Noise Controls ---
        self.noise_options = ["None", "Gaussian", "Salt & Pepper", "Both"]
        self.selected_noise = tk.StringVar(value=self.noise_options[0])
        noise_menu = ttk.Combobox(control_frame, textvariable=self.selected_noise, values=self.noise_options, state="readonly", width=18)
        noise_menu.pack(side=tk.LEFT, padx=10)

        tk.Label(control_frame, text="Gauss sigma:").pack(side=tk.LEFT)
        self.gauss_sigma_var = tk.DoubleVar(value=25.0)
        gauss_entry = tk.Entry(control_frame, textvariable=self.gauss_sigma_var, width=6)
        gauss_entry.pack(side=tk.LEFT, padx=(2, 8))

        tk.Label(control_frame, text="SP amount:").pack(side=tk.LEFT)
        self.sp_amount_var = tk.DoubleVar(value=0.02)
        sp_entry = tk.Entry(control_frame, textvariable=self.sp_amount_var, width=6)
        sp_entry.pack(side=tk.LEFT, padx=(2, 8))

        btn_add_noise = tk.Button(control_frame, text="Add Noise", command=self.add_noise)
        btn_add_noise.pack(side=tk.LEFT, padx=6)

        btn_save_noisy = tk.Button(control_frame, text="Save Noisy", command=self.save_noisy)
        btn_save_noisy.pack(side=tk.LEFT, padx=6)

        btn_save_processed = tk.Button(control_frame, text="Save Processed", command=self.save_processed)
        btn_save_processed.pack(side=tk.LEFT, padx=6)

        # --- Metrics Display ---
        metrics_frame = tk.Frame(control_frame)
        metrics_frame.pack(side=tk.LEFT, padx=20)
        
        self.psnr_label = tk.Label(metrics_frame, text="PSNR: --", font=("Arial", 10))
        self.psnr_label.pack(side=tk.TOP)
        
        self.ssim_label = tk.Label(metrics_frame, text="SSIM: --", font=("Arial", 10))
        self.ssim_label.pack(side=tk.TOP)
        
        # Additional labels to show noisy metrics
        self.psnr_noisy_label = tk.Label(metrics_frame, text="PSNR (noisy): --", font=("Arial", 9))
        self.psnr_noisy_label.pack(side=tk.TOP)
        self.ssim_noisy_label = tk.Label(metrics_frame, text="SSIM (noisy): --", font=("Arial", 9))
        self.ssim_noisy_label.pack(side=tk.TOP)
    
    # --- NEW --- This function is called when a new filter is selected from the dropdown
    def on_filter_change(self, event=None):
        """Clears the processed image canvas when the filter selection changes."""
        if self.original_image is None:
            return # Do nothing if no image is loaded
            
        print(f"\nFilter selection changed to '{self.selected_filter.get()}'. Clearing view.")
        
        # Clear the canvas (no text overlay)
        self.canvas_processed.delete("all")
        
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

        # Reset noisy and processed
        self.noisy_image = None
        self.processed_image = None

        self.root.after(100, lambda: self.display_image(self.original_image, self.canvas_original))
        self.canvas_processed.delete("all")
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

        # decide source image (noisy if present)
        source = self.noisy_image if self.noisy_image is not None else self.original_image

        if choice == "Guided Filter":
            self.processed_image = self._guided_filter(source)
        elif choice == "Rolling Guidance Filter":
            self.processed_image = self._rolling_guidance_filter(source)
        elif choice == "Kuwahara Filter":
            self.processed_image = self._kuwahara_filter_vectorized(source)
        elif choice == "Kuwahara Filter (Entropy-based)":
            self.processed_image = self._kuwahara_entropy_filter(source)

        if self.processed_image is not None:
            print(f"'{choice}' filter applied successfully. Displaying result.")
            self.display_image(self.processed_image, self.canvas_processed)
            self._calculate_and_display_metrics()
        else:
            print(f"Filter '{choice}' failed to produce an output.")

    def _calculate_and_display_metrics(self):
        """Calculates PSNR and SSIM and updates the GUI labels."""
        # if no image loaded
        if self.original_image is None:
            return

        # show noisy metrics if noisy image exists
        if self.noisy_image is not None:
            try:
                noisy_resized = cv2.resize(self.noisy_image, (self.original_image.shape[1], self.original_image.shape[0]))
                psnr_noisy = psnr(self.original_image, noisy_resized, data_range=255)
                try:
                    ssim_noisy = ssim(self.original_image, noisy_resized, data_range=255, channel_axis=2)
                except TypeError:
                    ssim_noisy = ssim(self.original_image, noisy_resized, data_range=255, multichannel=True)
                self.psnr_noisy_label.config(text=f"PSNR (noisy): {psnr_noisy:.2f} dB")
                self.ssim_noisy_label.config(text=f"SSIM (noisy): {ssim_noisy:.4f}")
            except Exception:
                self.psnr_noisy_label.config(text="PSNR (noisy): --")
                self.ssim_noisy_label.config(text="SSIM (noisy): --")
        else:
            self.psnr_noisy_label.config(text="PSNR (noisy): --")
            self.ssim_noisy_label.config(text="SSIM (noisy): --")

        if self.processed_image is None:
            self.psnr_label.config(text="PSNR: --")
            self.ssim_label.config(text="SSIM: --")
            return

        h, w, _ = self.original_image.shape
        processed_resized = cv2.resize(self.processed_image, (w, h))

        psnr_value = psnr(self.original_image, processed_resized, data_range=255)
        try:
            ssim_value = ssim(self.original_image, processed_resized, data_range=255, channel_axis=2)
        except TypeError:
            ssim_value = ssim(self.original_image, processed_resized, data_range=255, multichannel=True)

        self.psnr_label.config(text=f"PSNR: {psnr_value:.2f} dB")
        self.ssim_label.config(text=f"SSIM: {ssim_value:.4f}")
        print(f"Metrics Calculated -> PSNR: {psnr_value:.2f} dB, SSIM: {ssim_value:.4f}")

        # Also print improvement over noisy (if noisy exists)
        if self.noisy_image is not None:
            try:
                noisy_resized = cv2.resize(self.noisy_image, (w, h))
                psnr_noisy = psnr(self.original_image, noisy_resized, data_range=255)
                print(f"Improvement vs noisy -> PSNR delta: {psnr_value - psnr_noisy:+.2f} dB")
            except Exception:
                pass

    # --- Filter Implementations ---

    def _local_entropy(self, image, window_size=5, bins=64):
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

    def _kuwahara_entropy_single_channel(self, image, window_size=5, bins=64):
        """Entropy-based Kuwahara filter for single channel."""
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
        ent_tl = self._local_entropy(image, window_size, bins)[pad:, pad:]
        ent_tr = self._local_entropy(image[:, ::-1], window_size, bins)[pad:, pad:][:, ::-1]
        ent_bl = self._local_entropy(image[::-1, :], window_size, bins)[pad:, pad:][::-1, :]
        ent_br = self._local_entropy(image[::-1, ::-1], window_size, bins)[pad:, pad:][::-1, ::-1]

        ent_tl, ent_tr, ent_bl, ent_br = [
            e[:h, :w] for e in (ent_tl, ent_tr, ent_bl, ent_br)
        ]

        # Stack and select best quadrant
        entropies = np.stack([ent_tl, ent_tr, ent_bl, ent_br], axis=-1)
        means = np.stack([mean_tl, mean_tr, mean_bl, mean_br], axis=-1)

        best_idx = np.argmin(entropies, axis=-1)
        output = np.take_along_axis(means, best_idx[..., None], axis=-1).squeeze(-1)

        return output

    def _kuwahara_entropy_filter(self, image, window_size=5):
        """Apply entropy-based Kuwahara filter to RGB image."""
        # Convert to float for processing
        img_float = image.astype(np.float32) / 255.0
        
        if img_float.ndim == 2:
            # Grayscale
            result = self._kuwahara_entropy_single_channel(img_float, window_size)
        else:
            # Process per channel
            result = np.stack(
                [self._kuwahara_entropy_single_channel(img_float[..., c], window_size) 
                 for c in range(img_float.shape[2])],
                axis=-1
            )
        
        # Convert back to uint8
        result = np.clip(result * 255, 0, 255).astype(np.uint8)
        return result

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

    # ---- Noise helpers and UI actions ----
    def add_noise(self):
        if self.original_image is None:
            print("Load an image first before adding noise.")
            return

        choice = self.selected_noise.get()
        sigma = float(self.gauss_sigma_var.get())
        sp_amount = float(self.sp_amount_var.get())

        img = self.original_image.copy()

        if choice == "None":
            self.noisy_image = None
            print("No noise added.")
            # clear noisy canvas
            self.canvas_processed.delete("all")
            self._calculate_and_display_metrics()
            return

        noisy = img.copy()
        if choice in ("Gaussian", "Both"):
            noisy = self._add_gaussian_noise(noisy, sigma=sigma)
        if choice in ("Salt & Pepper", "Both"):
            noisy = self._add_salt_pepper_noise(noisy, amount=sp_amount)

        self.noisy_image = noisy
        print(f"Added noise: {choice} (sigma={sigma}, sp_amount={sp_amount})")
        self.display_image(self.noisy_image, self.canvas_processed)
        self._calculate_and_display_metrics()

    def _add_gaussian_noise(self, img, mean=0.0, sigma=25.0):
        if img.dtype != np.uint8:
            img = img.astype(np.uint8)
        row, col, ch = img.shape
        gauss = np.random.normal(mean, sigma, (row, col, ch)).reshape(row, col, ch)
        noisy = img.astype(np.float32) + gauss
        noisy = np.clip(noisy, 0, 255).astype(np.uint8)
        return noisy

    def _add_salt_pepper_noise(self, img, amount=0.02):
        out = img.copy()
        num_pixels = int(amount * img.shape[0] * img.shape[1])
        coords = [np.random.randint(0, i - 1, num_pixels) for i in img.shape[:2]]
        out[coords[0], coords[1]] = 255
        coords = [np.random.randint(0, i - 1, num_pixels) for i in img.shape[:2]]
        out[coords[0], coords[1]] = 0
        return out

    def save_noisy(self):
        if getattr(self, 'noisy_image', None) is None:
            print("No noisy image to save.")
            return
        # Ensure outputs directory exists
        os.makedirs('outputs', exist_ok=True)
        save_path = filedialog.asksaveasfilename(
            initialdir='outputs',
            initialfile='noisy.png',
            defaultextension='.png', 
            filetypes=[('PNG','*.png'),('JPEG','*.jpg;*.jpeg')]
        )
        if not save_path:
            return
        bgr = cv2.cvtColor(self.noisy_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(save_path, bgr)
        print(f"Saved noisy image to {save_path}")

    def save_processed(self):
        if getattr(self, 'processed_image', None) is None:
            print("No processed image to save.")
            return
        # Ensure outputs directory exists
        os.makedirs('outputs', exist_ok=True)
        # Generate default filename based on selected filter
        filter_name = self.selected_filter.get().lower().replace(' ', '_').replace('-', '')
        default_name = f"{filter_name}.png"
        save_path = filedialog.asksaveasfilename(
            initialdir='outputs',
            initialfile=default_name,
            defaultextension='.png', 
            filetypes=[('PNG','*.png'),('JPEG','*.jpg;*.jpeg')]
        )
        if not save_path:
            return
        bgr = cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(save_path, bgr)
        print(f"Saved processed image to {save_path}")

# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageFilterApp(root)
    root.mainloop()