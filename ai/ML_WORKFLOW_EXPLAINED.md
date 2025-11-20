# ML System Workflow Explained

## Two-Phase System

Your ML system has **two separate phases**:

### Phase 1: Training (Create/Update Models)
**File:** `train_with_real_data.py` (or other training scripts)

```
Database → Training Script → Model Files (.pkl)
```

**What happens:**
1. Connects to your database
2. Fetches real sensor readings (TDS, Turbidity)
3. Trains ML models on that data
4. Saves models as `.pkl` files:
   - `potability_classifier.pkl`
   - `potability_score_regressor.pkl`

**When to run:**
- Initially: To create models
- Periodically: To retrain with new data (weekly/monthly)
- When you have enough new data (50+ readings)

**Command:**
```bash
python train_with_real_data.py
```

---

### Phase 2: Serving (Use Models for Predictions)
**File:** `ml_server.py`

```
API Request → ml_server.py → Load Models → Return Prediction
```

**What happens:**
1. Loads the trained `.pkl` model files
2. Starts Flask web server
3. Accepts HTTP requests with water quality parameters
4. Returns potability predictions

**When to run:**
- Continuously: Keep this running as a service
- After training: Start this to serve predictions
- For deployment: Deploy this to Heroku/cloud

**Command:**
```bash
python ml_server.py
```

---

## Complete Workflow

```
┌─────────────────────────────────────────────────────────┐
│  STEP 1: TRAIN MODELS (One-time or Periodic)          │
│  ────────────────────────────────────────────────────  │
│                                                         │
│  Database (Real Sensor Data)                          │
│         ↓                                               │
│  train_with_real_data.py                               │
│         ↓                                               │
│  potability_classifier.pkl                             │
│  potability_score_regressor.pkl                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 2: SERVE PREDICTIONS (Continuous)                │
│  ────────────────────────────────────────────────────  │
│                                                         │
│  potability_classifier.pkl                             │
│  potability_score_regressor.pkl                         │
│         ↓                                               │
│  ml_server.py (Flask API)                               │
│         ↓                                               │
│  HTTP Requests → Predictions                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Why Two Separate Files?

### Separation of Concerns
- **Training** = Heavy computation, runs occasionally
- **Serving** = Lightweight, runs continuously

### Benefits:
1. **Efficiency**: Don't retrain every time you need a prediction
2. **Flexibility**: Update models without restarting the API
3. **Scalability**: Can run training on a different machine
4. **Deployment**: Only deploy `ml_server.py` to production

---

## Your Training Scripts

You have multiple training scripts for different purposes:

| Script | Purpose | Data Source |
|--------|---------|-------------|
| `train_with_real_data.py` | Train with real DB data | Database (TDS/Turbidity) |
| `train_potability_recommendation.py` | Train potability models | Synthetic data |
| `train_with_real_db_data.py` | Train potability with DB | Database |
| `simple_train.py` | Quick demo training | Synthetic data |
| `train_windows.py` | Windows-friendly training | Synthetic data |

**Recommendation:** Use `train_potability_recommendation.py` for potability models that `ml_server.py` uses.

---

## Quick Start Guide

### First Time Setup:

1. **Train the models:**
   ```bash
   cd ai
   python train_potability_recommendation.py
   ```
   This creates: `potability_classifier.pkl` and `potability_score_regressor.pkl`

2. **Start the API server:**
   ```bash
   python ml_server.py
   ```
   Server starts on `http://localhost:5000`

3. **Test the API:**
   ```bash
   curl http://localhost:5000/predict?tds=350&turbidity=0.8
   ```

### Updating Models:

1. **Retrain with new data:**
   ```bash
   python train_with_real_db_data.py
   ```

2. **Restart the server:**
   ```bash
   # Stop current server (Ctrl+C)
   python ml_server.py
   ```

---

## Common Questions

**Q: Do I need to run training every time?**
A: No! Only when you want to update models with new data.

**Q: Can I run both at the same time?**
A: Yes, but training will lock the model files. Better to train, then restart the server.

**Q: Which training script should I use?**
A: 
- For potability: `train_potability_recommendation.py`
- For real data: `train_with_real_db_data.py`
- For quick demo: `simple_train.py`

**Q: What if models don't load?**
A: The API will still work using rule-based classification (WHO guidelines) as fallback.

---

## File Summary

| File | Type | Purpose |
|------|------|---------|
| `ml_server.py` | **Server** | Serves predictions via API |
| `train_with_real_data.py` | **Training** | Trains TDS/Turbidity models |
| `train_potability_recommendation.py` | **Training** | Trains potability models |
| `*.pkl` files | **Models** | Trained model files (created by training scripts) |

---

## Next Steps

1. ✅ Train models: `python train_potability_recommendation.py`
2. ✅ Start server: `python ml_server.py`
3. ✅ Test API: Visit `http://localhost:5000/predict?tds=350&turbidity=0.8`
4. ✅ Deploy: Follow `HEROKU_DEPLOYMENT.md` for Heroku deployment


