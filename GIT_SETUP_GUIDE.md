# 🚀 Complete Setup & Git Instructions

## ✅ FIRST: Understanding What NOT to Commit

**NEVER commit `.venv/` folder to git!** It contains thousands of dependency files (100MB+) and should be ignored.

The `.gitignore` file I created handles this automatically.

---

## 📋 Step-by-Step Instructions

### **PART 1: Git Setup (Already Done!)**

The `.gitignore` file is now in place. Here's what it excludes:
- ✅ `.venv/` folder (virtual environment)
- ✅ `__pycache__/` (Python cache)
- ✅ `archive/` folder (old dev files)
- ✅ Generated output images (but keeps test images)

### **PART 2: Commit Your Changes**

Run these commands one by one:

```powershell
# 1. Add the .gitignore file first
git add .gitignore

# 2. Add your main project files
git add app.py requirements.txt

# 3. Add documentation files
git add README.md QUICK_START.md PRESENTATION_GUIDE.md CLEANUP_GUIDE.md

# 4. Add test images
git add images.jpeg images/

# 5. Check what will be committed (should NOT include .venv)
git status

# 6. Commit with a descriptive message
git commit -m "Integrate entropy-based Kuwahara filter and add comprehensive documentation"

# 7. Push to GitHub
git push origin tanishq
```

---

## 🔧 For Someone Cloning Your Repository

When someone clones your repo, they need to:

### **Step 1: Clone the Repository**
```powershell
git clone https://github.com/oxo-crab/FCV-proj.git
cd FCV-proj
git checkout tanishq
```

### **Step 2: Create Virtual Environment**
```powershell
python -m venv .venv
```

### **Step 3: Activate Virtual Environment**
```powershell
.\.venv\Scripts\Activate.ps1
```

### **Step 4: Install Dependencies**
```powershell
pip install -r requirements.txt
```

### **Step 5: Run the Application**
```powershell
python app.py
```

---

## 📝 What's Included in Git

### ✅ Files INCLUDED:
- `app.py` - Main application
- `requirements.txt` - Dependencies list
- `images.jpeg` - Test image
- `images/` folder - Additional test images
- `README.md` - Technical overview
- `QUICK_START.md` - Quick setup guide
- `PRESENTATION_GUIDE.md` - Demo instructions
- `CLEANUP_GUIDE.md` - File organization
- `.gitignore` - Git ignore rules

### ❌ Files EXCLUDED (by .gitignore):
- `.venv/` - Virtual environment (100MB+)
- `__pycache__/` - Python cache
- `archive/` - Old development files
- `outputs/` - Generated output images (optional)
- Generated `.jpg/.png` files (except test images)

---

## 🎯 Why We Don't Commit .venv

**Size:** The `.venv` folder contains **thousands of files** (100MB+)
- Makes git slow
- Makes cloning slow
- Different OS/Python versions may conflict
- Wastes GitHub storage

**Instead:** Use `requirements.txt`
- Small text file (< 1KB)
- Anyone can recreate the environment with `pip install -r requirements.txt`
- Cross-platform compatible

---

## 🔍 Verifying Your Commit

After running `git status`, you should see:

**✅ GOOD:**
```
Changes to be committed:
        new file:   .gitignore
        modified:   app.py
        new file:   CLEANUP_GUIDE.md
        new file:   images.jpeg
        new file:   images/a.jpg
        new file:   PRESENTATION_GUIDE.md
        new file:   QUICK_START.md
        new file:   README.md
        modified:   requirements.txt
```

**❌ BAD (if you see this, run `git reset`):**
```
        new file:   .venv/Lib/site-packages/...
        new file:   .venv/Scripts/...
        (thousands of .venv files)
```

---

## 🆘 If You Already Committed .venv

If you accidentally committed `.venv`, fix it:

```powershell
# Remove .venv from git tracking (keeps local files)
git rm -r --cached .venv

# Add .gitignore
git add .gitignore

# Commit the fix
git commit -m "Remove .venv from tracking and add .gitignore"

# Push
git push origin tanishq --force
```

---

## 📦 Summary: Git Workflow

```powershell
# Daily workflow:
git status                    # Check what changed
git add <files>              # Stage specific files
git commit -m "message"      # Commit with message
git push origin tanishq      # Push to GitHub

# Never do:
git add .                    # Without .gitignore (adds everything!)
git add .venv/              # Manually adding venv
```

---

## ✨ Quick Reference Commands

### Check Status
```powershell
git status              # What's changed?
git log --oneline      # Recent commits
git diff               # What changed in files?
```

### Add Files
```powershell
git add file.py                    # Add specific file
git add *.md                       # Add all markdown
git add .                          # Add all (safe with .gitignore)
```

### Commit & Push
```powershell
git commit -m "Your message"       # Commit staged files
git push origin tanishq           # Push to GitHub
```

### Undo Changes
```powershell
git reset                          # Unstage all
git reset file.py                  # Unstage specific file
git restore file.py               # Discard local changes
git rm --cached file.py           # Remove from git (keep local)
```

---

## 🎓 For Your Presentation

When showing your teacher:

1. **Show the GitHub repo** (clean, no .venv clutter)
2. **Clone it fresh** (demonstrates portability)
3. **Run setup commands** (shows reproducibility)
4. **Launch app** (works perfectly)

This proves:
✅ Proper version control practices
✅ Reproducible environment
✅ Professional project structure

---

## 🚨 Common Mistakes to Avoid

1. ❌ `git add .` without `.gitignore` → Adds everything including .venv
2. ❌ Committing output images → Bloats repository
3. ❌ Hardcoding paths → Won't work on other machines
4. ❌ Not testing clone → Might be missing files

**Always:**
✅ Use `.gitignore`
✅ Test by cloning in a new folder
✅ Keep commits focused and meaningful
✅ Use `git status` before committing

---

## 📞 Need Help?

If something goes wrong:
1. **Check git status:** `git status`
2. **Reset if needed:** `git reset`
3. **Re-add properly:** Follow commands above
4. **Verify:** No `.venv` files should appear

---

**You're all set! Your repository is now clean and professional! 🎉**
