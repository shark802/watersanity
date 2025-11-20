# How to Auto-Load Models on Heroku

## ✅ Current Status

Your models **ARE** tracked in Git:
- ✅ `ai/potability_classifier.pkl`
- ✅ `ai/potability_score_regressor.pkl`
- ✅ Other model files

Your code **ALREADY** auto-loads models:
- ✅ `ml_server.py` calls `load_models()` automatically (line 70)
- ✅ Models load when the module is imported (for gunicorn)

## Why Models Might Not Be Loading

If `models_loaded: false` on Heroku, check:

### 1. Models Not Pushed to Heroku

**Check if models are in Heroku:**
```bash
heroku run ls -la ai/*.pkl
```

**If missing, push them:**
```bash
git add ai/*.pkl
git commit -m "Add ML models"
git push heroku main
```

### 2. File Size Limits

Heroku has a **500MB slug size limit**. Large model files might be excluded.

**Check model sizes:**
```bash
# Windows PowerShell
Get-ChildItem ai\*.pkl | Select-Object Name, @{Name="Size(MB)";Expression={[math]::Round($_.Length/1MB,2)}}
```

**If models are too large (>100MB each):**
- Consider using Git LFS (Large File Storage)
- Or use external storage (AWS S3, etc.)

### 3. Path Issues

The models should be in the `ai/` directory relative to `ml_server.py`.

**Verify on Heroku:**
```bash
heroku run python -c "import os; print(os.listdir('ai'))"
```

## Solution: Force Include Models

### Step 1: Verify Models Are Committed

```bash
git status ai/*.pkl
```

Should show: "nothing to commit" (already tracked)

### Step 2: Ensure They're Not Ignored

Check `.gitignore` - make sure these lines are **commented out**:
```gitignore
# Model files (optional - uncomment if you don't want to commit models)
# *.pkl          ← Should be commented (with #)
# ai/*.pkl       ← Should be commented (with #)
```

### Step 3: Push to Heroku

```bash
# Make sure models are committed
git add ai/potability_classifier.pkl ai/potability_score_regressor.pkl
git commit -m "Ensure ML models are included"

# Push to Heroku
git push heroku main
```

### Step 4: Verify Models Load

After deployment, check:
```bash
curl https://endpoint-watersanity-4ea340547d1f.herokuapp.com/health
```

Should show: `"models_loaded": true`

## Alternative: Use Git LFS for Large Models

If models are too large (>100MB):

### 1. Install Git LFS
```bash
git lfs install
```

### 2. Track .pkl files with LFS
```bash
git lfs track "*.pkl"
git add .gitattributes
git add ai/*.pkl
git commit -m "Track models with Git LFS"
```

### 3. Push to Heroku
```bash
git push heroku main
```

**Note:** Heroku supports Git LFS, but you may need to install the buildpack:
```bash
heroku buildpacks:add https://github.com/raxod502/heroku-buildpack-git-lfs
```

## Quick Fix: Re-deploy Everything

If models still don't load, force a complete redeploy:

```bash
# 1. Make sure everything is committed
git add .
git commit -m "Full deployment with models"

# 2. Push to Heroku
git push heroku main --force

# 3. Check logs
heroku logs --tail

# 4. Verify models loaded
curl https://endpoint-watersanity-4ea340547d1f.herokuapp.com/health
```

## Debugging: Check Heroku Logs

```bash
heroku logs --tail
```

Look for:
- `✅ Potability Classifier loaded successfully`
- `✅ Score Regressor loaded successfully`
- `✅ All AI models loaded and ready!`

Or errors like:
- `❌ Potability Classifier not found`
- `[DEBUG] Files in directory: [...]`

## Expected Behavior

When you deploy, models should automatically load because:

1. ✅ Models are in Git (tracked)
2. ✅ `.gitignore` doesn't exclude them
3. ✅ `ml_server.py` auto-loads on import (line 70)
4. ✅ Heroku deploys all committed files

After `git push heroku main`, the models should load automatically!

## Verify It Worked

After deployment:
```bash
# Check health
curl https://endpoint-watersanity-4ea340547d1f.herokuapp.com/health

# Should return:
# {"models_loaded": true, "status": "healthy", ...}
```

---

**TL;DR:** Your models are already set up to auto-load! Just make sure they're pushed to Heroku with `git push heroku main`.


