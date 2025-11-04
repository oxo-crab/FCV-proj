# Project Cleanup & Organization Guide

## Current Status
Your project has been updated! The entropy-based Kuwahara filter from `edited.py` is now integrated into `app.py`.

---

## 📁 File Organization Plan

### ✅ **KEEP - Main Project Files**
These are essential for your presentation:

1. **`app.py`** ⭐ - Main GUI application (now includes all filters)
2. **`requirements.txt`** - Dependencies list
3. **`images.jpeg`** - Your test/noisy image
4. **`images/`** folder - Keep for additional test images
5. **`outputs/`** folder - All processed results go here

### 🗑️ **DELETE or ARCHIVE - Development/Test Files**

**Option A: Delete these files (if you're confident):**
```powershell
Remove-Item edited.py
Remove-Item edited_kuwahara.py
Remove-Item noise_demo.py
Remove-Item ml_impact_test.py
Remove-Item kuwahara_entropy_color.jpg
Remove-Item kuwahara_entropy_gray.jpg
```

**Option B: Archive them (safer - create backup):**
```powershell
# Create archive folder
New-Item -ItemType Directory -Path "archive" -Force

# Move files to archive
Move-Item edited.py archive/
Move-Item edited_kuwahara.py archive/
Move-Item noise_demo.py archive/
Move-Item ml_impact_test.py archive/
Move-Item kuwahara_entropy_color.jpg archive/ -ErrorAction SilentlyContinue
Move-Item kuwahara_entropy_gray.jpg archive/ -ErrorAction SilentlyContinue
Move-Item median_kuwahara_output.png archive/ -ErrorAction SilentlyContinue
```

### 🔄 **OPTIONAL - Clean up cache files**
```powershell
# Remove Python cache
Remove-Item -Recurse -Force __pycache__
```

---

## 📂 Final Clean Project Structure

After cleanup, your project should look like:
```
FCV-proj/
├── app.py                    # Main GUI application ⭐
├── requirements.txt          # Dependencies
├── images.jpeg              # Test image
├── images/                  # Additional test images
│   └── a.jpg
├── outputs/                 # All processed results
│   ├── noisy.png
│   ├── guided_filter.png
│   ├── rolling_guidance.png
│   ├── kuwahara_vectorized.png
│   ├── kuwahara_filter_(entropybased).png
│   ├── gaussian_blur.png
│   └── median_kuwahara.png
└── archive/                 # (Optional) Old development files
```

---

## 🎯 What Changed in app.py

### New Features Added:
1. **Entropy-based Kuwahara Filter** - Advanced noise reduction using entropy
2. **Auto-save to outputs/** - All saves default to the outputs folder
3. **Smart file naming** - Processed images auto-named by filter type

### Available Filters:
1. Guided Filter
2. Rolling Guidance Filter
3. Kuwahara Filter (variance-based)
4. **Kuwahara Filter (Entropy-based)** ⭐ NEW
5. Portrait - Standard Blur
6. Portrait - Artistic Style

---

## ✅ Quick Cleanup Commands

**Recommended: Archive old files**
```powershell
New-Item -ItemType Directory -Path "archive" -Force
Move-Item edited.py, edited_kuwahara.py, noise_demo.py, ml_impact_test.py archive/
Move-Item *.jpg archive/ -ErrorAction SilentlyContinue -Exclude "images.jpeg"
Remove-Item -Recurse -Force __pycache__
```

This keeps everything safe while presenting a clean project!
