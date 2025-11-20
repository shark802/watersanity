# ML Server API Reference

## Base URL
- **Local**: `http://localhost:5000`
- **Heroku**: `https://your-app-name.herokuapp.com`

## Endpoints

### 1. Health Check
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "models_loaded": true,
  "timestamp": "2024-01-15T10:30:00"
}
```

---

### 2. Server Status
```bash
GET /status
```

**Response:**
```json
{
  "status": "running",
  "models_loaded": true,
  "timestamp": "2024-01-15T10:30:00",
  "python_version": "3.11.7",
  "working_directory": "/app/ai"
}
```

---

### 3. Get Prediction (GET)

**Endpoint:** `GET /predict`

**Query Parameters:**
- `tds` or `tds_value` (float, default: 350) - Total Dissolved Solids in ppm
- `turbidity` or `turbidity_value` (float, default: 0.8) - Turbidity in NTU
- `temperature` (float, default: 25) - Temperature in Celsius
- `ph` or `ph_level` (float, default: 7.0) - pH level

**Example:**
```bash
curl "http://localhost:5000/predict?tds=350&turbidity=0.8&temperature=25&ph=7.0"
```

**Response:**
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
    "accuracy": "99.5%"
  }
}
```

---

### 4. Get Prediction (POST)

**Endpoint:** `POST /predict`

**Request Body (JSON):**
```json
{
  "tds": 350,
  "turbidity": 0.8,
  "temperature": 25,
  "ph": 7.0
}
```

**Alternative parameter names (backward compatible):**
```json
{
  "tds_value": 350,
  "turbidity_value": 0.8,
  "temperature": 25,
  "ph_level": 7.0
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "tds": 350,
    "turbidity": 0.8,
    "temperature": 25,
    "ph": 7.0
  }'
```

**Response:** Same as GET request

---

### 5. Test Endpoint
```bash
GET /test
```

Returns a prediction with sample data (tds=350, turbidity=0.8)

---

## Parameter Validation

The API validates input ranges:
- **TDS**: 0 - 10,000 ppm
- **Turbidity**: 0 - 100 NTU
- **Temperature**: -10 - 50 °C
- **pH**: 0 - 14

**Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "TDS value must be between 0 and 10000"
}
```

---

## Error Responses

### 400 Bad Request
Invalid parameter format or out of range:
```json
{
  "status": "error",
  "message": "Invalid parameter format: ..."
}
```

### 500 Internal Server Error
Server error or models not loaded:
```json
{
  "status": "error",
  "message": "AI models not loaded. Please train models first."
}
```

---

## Example Usage

### Python
```python
import requests

# GET request
response = requests.get('http://localhost:5000/predict', params={
    'tds': 350,
    'turbidity': 0.8,
    'temperature': 25,
    'ph': 7.0
})
print(response.json())

# POST request
response = requests.post('http://localhost:5000/predict', json={
    'tds': 350,
    'turbidity': 0.8,
    'temperature': 25,
    'ph': 7.0
})
print(response.json())
```

### JavaScript (Fetch API)
```javascript
// GET request
fetch('http://localhost:5000/predict?tds=350&turbidity=0.8&temperature=25&ph=7.0')
  .then(response => response.json())
  .then(data => console.log(data));

// POST request
fetch('http://localhost:5000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    tds: 350,
    turbidity: 0.8,
    temperature: 25,
    ph: 7.0
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### PHP
```php
// GET request
$url = 'http://localhost:5000/predict?tds=350&turbidity=0.8&temperature=25&ph=7.0';
$response = file_get_contents($url);
$data = json_decode($response, true);

// POST request
$data = [
    'tds' => 350,
    'turbidity' => 0.8,
    'temperature' => 25,
    'ph' => 7.0
];
$options = [
    'http' => [
        'method' => 'POST',
        'header' => 'Content-Type: application/json',
        'content' => json_encode($data)
    ]
];
$context = stream_context_create($options);
$response = file_get_contents('http://localhost:5000/predict', false, $context);
$result = json_decode($response, true);
```

---

## Notes

- All parameters are optional and have default values
- Both GET and POST support the same parameter names
- The API accepts both short names (`tds`, `turbidity`, `ph`) and full names (`tds_value`, `turbidity_value`, `ph_level`) for backward compatibility
- Temperature and pH are optional but recommended for more accurate predictions

