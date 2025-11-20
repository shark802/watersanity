# Water Potability AI System - Architecture Documentation

## System Overview

Your system follows a **3-tier architecture** with PHP middleware connecting the database to the Python ML server.

---

## Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PHP SYSTEM (Middleware Layer)                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    DATABASE LAYER                             │   │
│  │  ┌──────────────┐         ┌──────────────┐                   │   │
│  │  │   MySQL      │◄────────┤  db.php      │                   │   │
│  │  │  Database    │         │  $conn       │                   │   │
│  │  │              │         └──────────────┘                   │   │
│  │  │ Tables:      │                                             │   │
│  │  │ • tds_readings│                                            │   │
│  │  │ • turbidity_ │                                            │   │
│  │  │   readings   │                                            │   │
│  │  └──────┬───────┘                                             │   │
│  └────────┼─────────────────────────────────────────────────────┘   │
│           │                                                          │
│           │ SELECT sensor data                                      │
│           ▼                                                          │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              PHP DATA ACCESS LAYER                           │   │
│  │  ┌──────────────────────────────────────┐                    │   │
│  │  │  device/tds/tds_receiver.php        │                    │   │
│  │  │  - Receives ESP32 sensor data       │                    │   │
│  │  │  - Inserts into tds_readings        │                    │   │
│  │  │  - Inserts into turbidity_readings  │                    │   │
│  │  └──────────────────────────────────────┘                    │   │
│  │                                                               │   │
│  │  ┌──────────────────────────────────────┐                    │   │
│  │  │  api/python_ml_server.php            │                    │   │
│  │  │  - Reads from database (optional)    │                    │   │
│  │  │  - Extracts: tds_value, turbidity    │                    │   │
│  │  │  - Calls Python ML Server           │                    │   │
│  │  └──────────────────────────────────────┘                    │   │
│  └──────────┬───────────────────────────────────────────────────┘   │
│             │                                                        │
│             │ HTTP Request (GET/POST)                                │
│             │ Parameters: tds, turbidity, temperature, ph           │
│             ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              PYTHON ML SERVER (Port 5000)                    │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  ai/ml_server.py                                      │   │   │
│  │  │  Flask Application                                   │   │   │
│  │  │                                                       │   │   │
│  │  │  ┌──────────────────────────────────────────────┐    │   │   │
│  │  │  │  AI RECOMMENDATION ENGINE                    │    │   │   │
│  │  │  │  get_potability_recommendation()            │    │   │   │
│  │  │  │                                              │    │   │   │
│  │  │  │  Uses:                                       │    │   │   │
│  │  │  │  • potability_classifier.pkl (ML Model)     │    │   │   │
│  │  │  │  • potability_score_regressor.pkl (ML)      │    │   │   │
│  │  │  │  • WHO Guidelines (Rule-based fallback)     │    │   │   │
│  │  │  │                                              │    │   │   │
│  │  │  │  Returns JSON:                              │    │   │   │
│  │  │  │  ✅ potability_status (Potable/Not Potable) │    │   │   │
│  │  │  │  ✅ potability_score (0-100%)              │    │   │   │
│  │  │  │  ✅ recommendation (text advice)           │    │   │   │
│  │  │  │  ✅ risk_level (Low/High)                  │    │   │   │
│  │  │  │  ✅ action_required                        │    │   │   │
│  │  │  │  ✅ who_compliance (tds/turbidity)         │    │   │   │
│  │  │  └──────────────────────────────────────────────┘    │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  └──────────┬───────────────────────────────────────────────────┘   │
│             │                                                        │
│             │ JSON Response with AI Recommendations                  │
│             ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              FRONTEND LAYER (JavaScript/HTML)                │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  device/tds/dashboard.php                            │   │   │
│  │  │  - Displays potability_score (%)                     │   │   │
│  │  │  - Shows potability_status                          │   │   │
│  │  │  - Displays AI recommendation                       │   │   │
│  │  │  - Shows risk_level and action_required             │   │   │
│  │  │  - Visual indicators (green/yellow/red)            │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### Flow 1: Sensor Data Collection
```
ESP32 Device
    ↓ (HTTP POST)
device/tds/tds_receiver.php
    ↓ (INSERT INTO)
MySQL Database
    ├─ tds_readings (tds_value, reading_time)
    └─ turbidity_readings (ntu_value, reading_time)
```

### Flow 2: AI Prediction Request
```
Frontend (JavaScript)
    ↓ (AJAX/Fetch)
api/python_ml_server.php
    ├─ Option 1: Read from database (if use_sensor=true)
    │   └─ SELECT latest tds_value, ntu_value
    │
    └─ Option 2: Use provided parameters
        └─ tds, turbidity, temperature, ph
    ↓ (HTTP GET)
ai/ml_server.py (Flask API)
    ├─ Load ML models (.pkl files)
    ├─ Process with get_potability_recommendation()
    └─ Return JSON response
    ↓ (JSON Response)
Frontend displays results
```

---

## File Structure & Responsibilities

### Database Layer
| File | Purpose |
|------|---------|
| `db.php` | Database connection configuration |
| MySQL Tables | `tds_readings`, `turbidity_readings` |

### PHP Middleware Layer
| File | Purpose |
|------|---------|
| `device/tds/tds_receiver.php` | Receives ESP32 sensor data, saves to DB |
| `api/python_ml_server.php` | **Main bridge** - connects PHP to Python ML server |
| `api/potability_recommendation.php` | Alternative PHP-only recommendation (fallback) |
| `api/predict_water_quality_online.php` | Predictive forecasting API |

### Python ML Layer
| File | Purpose |
|------|---------|
| `ai/ml_server.py` | **Main Flask API server** - serves predictions |
| `ai/train_potability_recommendation.py` | Trains ML models |
| `ai/potability_classifier.pkl` | Trained classification model |
| `ai/potability_score_regressor.pkl` | Trained scoring model |

### Frontend Layer
| File | Purpose |
|------|---------|
| `device/tds/dashboard.php` | Main dashboard displaying AI recommendations |

---

## API Endpoints

### Python ML Server (Port 5000)
- `GET /predict?tds=350&turbidity=0.8&temperature=25&ph=7.0`
- `POST /predict` (JSON body)
- `GET /health` - Health check
- `GET /status` - Server status

### PHP Bridge
- `GET api/python_ml_server.php?tds=350&turbidity=0.8&use_sensor=true`
- `POST api/python_ml_server.php` (JSON body)

---

## Configuration

### Local Development
```php
// api/python_ml_server.php
$python_server_url = 'http://localhost:5000';
```

### Production (After Heroku Deployment)
```php
// api/python_ml_server.php
$python_server_url = 'https://your-app-name.herokuapp.com';
```

---

## Request/Response Examples

### Request to PHP Bridge
```javascript
// Frontend JavaScript
fetch('api/python_ml_server.php?tds=350&turbidity=0.8&use_sensor=true')
  .then(response => response.json())
  .then(data => {
    console.log(data.potability_status);  // "Potable" or "Not Potable"
    console.log(data.potability_score);   // 0-100
    console.log(data.recommendation);     // Text advice
  });
```

### Response from ML Server
```json
{
  "status": "success",
  "potability_status": "Potable",
  "potability_score": 92.5,
  "confidence": 0.85,
  "risk_level": "Low",
  "recommendation": "Water is POTABLE. No immediate action needed.",
  "action_required": "None",
  "who_compliance": {
    "tds_compliant": true,
    "turbidity_compliant": true,
    "overall_compliant": true
  },
  "parameters": {
    "tds_value": 350,
    "turbidity_value": 0.8,
    "temperature": 25,
    "ph_level": 7.0
  },
  "who_guidelines": {
    "tds_limit": 500,
    "turbidity_limit": 1.0
  },
  "ai_info": {
    "model_version": "1.0",
    "training_date": "2024-10-21",
    "accuracy": "99.5%",
    "ml_models_loaded": true,
    "prediction_method": "ML Models"
  }
}
```

---

## System Requirements

### PHP Side
- PHP 7.4+
- MySQL/MariaDB
- `file_get_contents()` enabled (for HTTP requests)
- Or `curl` extension (preferred)

### Python Side
- Python 3.11+
- Flask
- scikit-learn
- joblib
- numpy, pandas

### Network
- Python ML server must be accessible from PHP
- Local: `localhost:5000`
- Production: Heroku URL or server IP

---

## Deployment Scenarios

### Scenario 1: Local Development
```
PHP (localhost) → Python ML Server (localhost:5000)
```

### Scenario 2: Production (Heroku)
```
PHP (your-server.com) → Python ML Server (your-app.herokuapp.com)
```

### Scenario 3: Same Server
```
PHP (your-server.com) → Python ML Server (your-server.com:5000)
```

---

## Troubleshooting

### Issue: "Python server not responding"
**Solution:**
1. Check if `ml_server.py` is running: `python ai/ml_server.py`
2. Verify port 5000 is accessible
3. Check firewall settings

### Issue: Models not loading
**Solution:**
1. Train models: `python ai/train_potability_recommendation.py`
2. Verify `.pkl` files exist in `ai/` directory
3. Check file permissions

### Issue: Database connection failed
**Solution:**
1. Verify `db.php` exists and has correct credentials
2. Check MySQL service is running
3. Verify database name and table names

---

## Next Steps

1. ✅ **Train Models**: Run `python ai/train_potability_recommendation.py`
2. ✅ **Start ML Server**: Run `python ai/ml_server.py`
3. ✅ **Test PHP Bridge**: Visit `api/python_ml_server.php?tds=350&turbidity=0.8`
4. ✅ **Deploy to Heroku**: Follow `HEROKU_DEPLOYMENT.md`
5. ✅ **Update PHP Bridge**: Change URL to Heroku endpoint

---

## Architecture Benefits

✅ **Separation of Concerns**: PHP handles web, Python handles ML  
✅ **Scalability**: Can deploy Python server separately  
✅ **Maintainability**: Clear boundaries between layers  
✅ **Flexibility**: Can swap ML models without changing PHP  
✅ **Performance**: ML server can be optimized independently  

---

This architecture is **production-ready** and follows best practices for ML integration!

