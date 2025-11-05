# Image Filter Workbench - FCV Mini Project# 🎨 Image Filter Workbench - FCV Mini Project



GUI application for image filtering and noise reduction with entropy-based Kuwahara filter.A comprehensive GUI application for comparing image filtering and noise reduction techniques, featuring an advanced **entropy-based Kuwahara filter**.



------



## Setup & Run## 🚀 Quick Start



### First Time Setup### Setup & Run (First Time)

```powershell```powershell

# Activate virtual environment# 1. Clone the repository (if needed)

.\.venv\Scripts\Activate.ps1git clone https://github.com/oxo-crab/FCV-proj.git

cd FCV-proj

# Install dependencies

pip install -r requirements.txt# 2. Create virtual environment (if .venv doesn't exist)

python -m venv .venv

# Run application

python app.py# 3. Activate virtual environment

```.\.venv\Scripts\Activate.ps1



### After Setup# 4. Install dependencies

```powershellpip install -r requirements.txt

.\.venv\Scripts\Activate.ps1

python app.py# 5. Run the application

```python app.py

```

### Real-time Metrics:
- **PSNR** (Peak Signal-to-Noise Ratio) - Measures pixel accuracy
- **SSIM** (Structural Similarity Index) - Measures perceptual quality
- Metrics for both noisy and filtered images

---


## 🎯 Key Innovation: Entropy-Based Kuwahara Filter

### What Makes It Special?
Traditional Kuwahara uses **variance** (spread of values) to select regions.  
Our implementation uses **Shannon entropy** (information content) instead.

### Why Entropy is Better:
**Better texture discrimination** - Distinguishes texture from noise  
**Superior preservation** - Keeps important details while smoothing  
**Higher PSNR/SSIM** - Achieves ~29 dB vs ~26-28 dB for other filters  
**Intelligent selection** - Chooses regions with most uniform information

### Algorithm Overview:
```python
For each pixel:
  1. Divide surrounding region into 4 quadrants
  2. Calculate Shannon entropy for each quadrant
  3. Select quadrant with MINIMUM entropy (most uniform)
  4. Use mean of selected quadrant as output pixel
```

---

## 📊 Expected Results

### Performance Comparison (from noisy ~20 dB):

| Filter | PSNR (dB) | SSIM | Processing Time |
|--------|-----------|------|-----------------|
| Noisy Image | ~20 | ~0.40 | - |
| Gaussian Blur | ~26 | ~0.78 | < 1s |
| Guided Filter | ~28 | ~0.85 | ~1s |
| Rolling Guidance | ~27 | ~0.83 | ~2s |
| Kuwahara (Standard) | ~26 | ~0.80 | ~2s |
| **Kuwahara (Entropy)** ⭐ | **~29** | **~0.87** | **2-5s** |

*Note: Results vary based on image content and noise levels*

---

## 📁 Project Structure

```
FCV-proj/
├── app.py                    # Main GUI application ⭐
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules (excludes .venv)
├── README.md                # This file
├── images.jpeg              # Sample test image
├── images/                  # Additional test images
│   └── a.jpg
├── outputs/                 # Processed results (auto-created)
│   ├── noisy.png
│   ├── guided_filter.png
│   ├── kuwahara_filter_(entropybased).png
│   └── ...
└── archive/                 # Old development files & extra docs
    ├── edited.py
    ├── PRESENTATION_GUIDE.md
    └── ...
```

---

## 🛠️ Technical Details

### Dependencies:
- **Python 3.9+** (tested on 3.9)
- **opencv-contrib-python** - Image processing & advanced filters
- **NumPy** - Array operations
- **scikit-image** - Metrics (PSNR, SSIM)
- **scikit-learn** - ML utilities
- **Pillow** - Image I/O
- **scipy** - Uniform filter for entropy calculation

### Installation:
```powershell
pip install -r requirements.txt
```



### Key Points :
Entropy measures information content, not just spread  
Better discrimination between noise and texture  
Achieves highest PSNR/SSIM among tested filters  
Real-world applications: Medical imaging, photography, satellite imagery  

### Some Common Questions:
**Q: Why entropy instead of variance?**  
A: Entropy measures information/disorder, making it better at distinguishing texture from noise. Variance only measures spread.

**Q: What's the computational cost?**  
A: ~2-5 seconds for 800x600 images. More intensive than variance but optimized with NumPy vectorization.

**Q: Real-world applications?**  
A: Medical imaging (preserving diagnostic details), photography (artistic effects), satellite imagery (feature enhancement).

---


### Proper Git Workflow:
```powershell
# Check status (verify no .venv files)
git status

# Add your changes
git add app.py requirements.txt README.md

# Commit
git commit -m "Your message"

# Push
git push origin tanishq
```

### For Someone Cloning:
```powershell
git clone <repo-url>
cd FCV-proj
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

---



---

## 📧 Credits

**Project:** FCV Mini Project - Image Filter Workbench  
**Institution:** MIT Manipal
**Course:** Fundamentals of Computer Vision (FCV)  
**Semester:** 5th Semester  
**Date:** November 2025  

**Team Members:**
- Jaypal Ashwin Nair    
- Tanishq Kochar
- Anubhab Basu 

---




## 🎉 Thank You!

