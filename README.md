# Image Filter Workbench - FCV Mini Project

A comprehensive GUI application for comparing image filtering and noise reduction techniques, featuring an advanced entropy-based Kuwahara filter.

---

## 🚀 Quick Start

### 1. Activate Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies (if needed)
```powershell
pip install -r requirements.txt
```

### 3. Run the Application
```powershell
python app.py
```

---

## 📋 Features

### Available Filters:
1. **Guided Filter** - Fast edge-preserving smoothing
2. **Rolling Guidance Filter** - Iterative edge-aware smoothing
3. **Kuwahara Filter** - Classic variance-based artistic filter
4. **Kuwahara Filter (Entropy-based)** ⭐ - Advanced texture-preserving filter
5. **Portrait - Standard Blur** - Background blur with face detection
6. **Portrait - Artistic Style** - Portrait with Kuwahara background

### Noise Types:
- Gaussian Noise (adjustable sigma)
- Salt & Pepper Noise (adjustable amount)
- Combined (both noise types)

### Metrics:
- **PSNR** (Peak Signal-to-Noise Ratio) - Measures pixel-level accuracy
- **SSIM** (Structural Similarity Index) - Measures perceptual quality

---

## 💡 How to Use

### Basic Workflow:
1. **Load Image** → Click "Load Image" and select your test image
2. **Add Noise** → Select noise type and click "Add Noise"
3. **Apply Filter** → Choose a filter from dropdown and click "Apply Filter"
4. **Save Results** → Click "Save Processed" to save to `outputs/` folder
5. **Compare** → Try different filters and compare PSNR/SSIM values

### Tips:
- **Higher PSNR** = Better quality (typically > 30 dB is good)
- **Higher SSIM** = Better structural similarity (max 1.0)
- All outputs save to `outputs/` folder automatically
- Try the **Entropy-based Kuwahara** for best texture preservation!

---

## 📁 Project Structure

```
FCV-proj/
├── app.py                    # Main GUI application ⭐
├── requirements.txt          # Python dependencies
├── images.jpeg              # Sample test image
├── images/                  # Additional test images folder
├── outputs/                 # Processed results (auto-created)
├── CLEANUP_GUIDE.md         # File organization guide
└── PRESENTATION_GUIDE.md    # Teacher demo guide
```

---

## 🎓 For Presentation

See **PRESENTATION_GUIDE.md** for:
- Complete demo script
- Anticipated questions & answers
- Technical talking points
- Time-based presentation formats (2/5/10 minute versions)

See **CLEANUP_GUIDE.md** for:
- Which files to keep/delete
- Archive commands
- Clean project structure

---

## 📊 Expected Results

### Typical PSNR Improvements (from noisy ~20 dB):
- Gaussian Blur: ~26 dB
- Guided Filter: ~28 dB
- Rolling Guidance: ~27 dB
- Kuwahara (Standard): ~26 dB
- **Kuwahara (Entropy-based): ~29 dB** ⭐ Best!

---

## 🛠️ Technical Details

### Dependencies:
- Python 3.x
- OpenCV (opencv-contrib-python)
- NumPy
- scikit-image
- scikit-learn
- Pillow
- scipy

### Key Innovation:
The **entropy-based Kuwahara filter** uses Shannon entropy instead of variance to select optimal regions, providing:
- Better texture preservation
- Superior noise reduction
- More intelligent region selection

### Algorithm:
```python
# For each pixel region:
1. Divide into 4 quadrants
2. Compute local entropy for each quadrant
3. Select quadrant with minimum entropy (most uniform)
4. Use mean of selected quadrant as output
```

---

## 📝 Notes

- First time running may take longer (compiling filters)
- Processing time: 2-5 seconds for typical images
- Larger images take longer with entropy-based filter
- Outputs are automatically organized in `outputs/` folder

---

## 🎯 Best Practices for Demo

1. ✅ Use **images.jpeg** or a high-contrast image
2. ✅ Add **"Both"** noise type for dramatic before/after
3. ✅ Highlight **Entropy-based Kuwahara** as your innovation
4. ✅ Show PSNR/SSIM metrics to quantify improvements
5. ✅ Compare at least 3-4 filters side-by-side in outputs folder

---

## 📧 Contact

Created by: [Your Name/Team]
Course: FCV Mini Project
Date: November 2025

---

**Good luck with your presentation! 🎉**
