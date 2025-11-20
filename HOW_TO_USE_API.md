# How to Use the ML Prediction API

## Quick Start

The API endpoint accepts water quality parameters and returns potability recommendations.

---

## Method 1: Direct Browser Access (Easiest)

### Local Development:
```
http://localhost:5000/predict?tds=350&turbidity=0.8&temperature=25&ph=7.0
```

### Production (Heroku):
```
https://endpoint-watersanity-4ea340547d1f.herokuapp.com/predict?tds=350&turbidity=0.8&temperature=25&ph=7.0
```

**Just paste this URL in your browser!** You'll see the JSON response.

---

## Method 2: Using cURL (Command Line)

### Windows (PowerShell):
```powershell
curl "http://localhost:5000/predict?tds=350&turbidity=0.8&temperature=25&ph=7.0"
```

### Windows (CMD):
```cmd
curl "http://localhost:5000/predict?tds=350&turbidity=0.8&temperature=25&ph=7.0"
```

### Linux/Mac:
```bash
curl "http://localhost:5000/predict?tds=350&turbidity=0.8&temperature=25&ph=7.0"
```

### With Pretty Print (jq):
```bash
curl "http://localhost:5000/predict?tds=350&turbidity=0.8" | jq
```

---

## Method 3: JavaScript (Frontend)

### Using Fetch API:
```javascript
// Simple GET request
fetch('http://localhost:5000/predict?tds=350&turbidity=0.8&temperature=25&ph=7.0')
  .then(response => response.json())
  .then(data => {
    console.log('Potability Status:', data.potability_status);
    console.log('Score:', data.potability_score);
    console.log('Recommendation:', data.recommendation);
    
    // Display on page
    document.getElementById('status').textContent = data.potability_status;
    document.getElementById('score').textContent = data.potability_score + '%';
    document.getElementById('recommendation').textContent = data.recommendation;
  })
  .catch(error => {
    console.error('Error:', error);
  });
```

### Using Axios:
```javascript
axios.get('http://localhost:5000/predict', {
  params: {
    tds: 350,
    turbidity: 0.8,
    temperature: 25,
    ph: 7.0
  }
})
.then(response => {
  console.log(response.data);
})
.catch(error => {
  console.error('Error:', error);
});
```

### Async/Await Version:
```javascript
async function getWaterQuality(tds, turbidity, temp = 25, ph = 7.0) {
  try {
    const response = await fetch(
      `http://localhost:5000/predict?tds=${tds}&turbidity=${turbidity}&temperature=${temp}&ph=${ph}`
    );
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    return null;
  }
}

// Usage
const result = await getWaterQuality(350, 0.8);
console.log(result);
```

---

## Method 4: PHP (Backend)

### Using file_get_contents:
```php
<?php
$tds = 350;
$turbidity = 0.8;
$temperature = 25;
$ph = 7.0;

$url = "http://localhost:5000/predict?tds={$tds}&turbidity={$turbidity}&temperature={$temperature}&ph={$ph}";

$response = file_get_contents($url);
$data = json_decode($response, true);

if ($data && $data['status'] === 'success') {
    echo "Status: " . $data['potability_status'] . "\n";
    echo "Score: " . $data['potability_score'] . "%\n";
    echo "Recommendation: " . $data['recommendation'] . "\n";
} else {
    echo "Error: " . ($data['message'] ?? 'Unknown error');
}
?>
```

### Using cURL (More Reliable):
```php
<?php
function getPotabilityPrediction($tds, $turbidity, $temperature = 25, $ph = 7.0) {
    $url = "http://localhost:5000/predict";
    $params = http_build_query([
        'tds' => $tds,
        'turbidity' => $turbidity,
        'temperature' => $temperature,
        'ph' => $ph
    ]);
    
    $ch = curl_init($url . '?' . $params);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode === 200) {
        return json_decode($response, true);
    }
    
    return ['status' => 'error', 'message' => 'API request failed'];
}

// Usage
$result = getPotabilityPrediction(350, 0.8);
print_r($result);
?>
```

---

## Method 5: Python

### Using requests library:
```python
import requests

url = "http://localhost:5000/predict"
params = {
    'tds': 350,
    'turbidity': 0.8,
    'temperature': 25,
    'ph': 7.0
}

response = requests.get(url, params=params)
data = response.json()

print(f"Status: {data['potability_status']}")
print(f"Score: {data['potability_score']}%")
print(f"Recommendation: {data['recommendation']}")
```

### Using urllib:
```python
import urllib.request
import json

url = "http://localhost:5000/predict?tds=350&turbidity=0.8&temperature=25&ph=7.0"

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())
    print(json.dumps(data, indent=2))
```

---

## Method 6: Using Your PHP Bridge

Instead of calling Python directly, use your PHP bridge:

```
http://your-server.com/api/python_ml_server.php?tds=350&turbidity=0.8&temperature=25&ph=7.0
```

This automatically:
- Detects if you're on localhost or production
- Connects to the correct Python server
- Handles errors gracefully

---

## Parameter Reference

| Parameter | Required | Default | Description | Range |
|-----------|----------|---------|-------------|-------|
| `tds` | No | 350 | Total Dissolved Solids (ppm) | 0-10000 |
| `turbidity` | No | 0.8 | Turbidity (NTU) | 0-100 |
| `temperature` | No | 25 | Temperature (°C) | -10 to 50 |
| `ph` | No | 7.0 | pH level | 0-14 |

**Note:** All parameters are optional. If omitted, defaults are used.

---

## Example Responses

### Success Response:
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

### Error Response:
```json
{
  "status": "error",
  "message": "TDS value must be between 0 and 10000"
}
```

---

## Real-World Examples

### Example 1: Check if water is safe
```javascript
// JavaScript
const checkWater = async (tds, turbidity) => {
  const response = await fetch(
    `http://localhost:5000/predict?tds=${tds}&turbidity=${turbidity}`
  );
  const data = await response.json();
  
  if (data.potability_status === 'Potable') {
    alert('✅ Water is safe to drink!');
  } else {
    alert('⚠️ Water is NOT safe. ' + data.recommendation);
  }
};

checkWater(350, 0.8);
```

### Example 2: Display on dashboard
```javascript
// Update dashboard every 30 seconds
setInterval(async () => {
  const response = await fetch(
    'http://localhost:5000/predict?tds=350&turbidity=0.8'
  );
  const data = await response.json();
  
  document.getElementById('potability-score').textContent = 
    data.potability_score + '%';
  document.getElementById('potability-status').textContent = 
    data.potability_status;
  document.getElementById('recommendation').textContent = 
    data.recommendation;
}, 30000);
```

### Example 3: Use sensor data from database
```php
// PHP - Get latest sensor readings and check potability
require_once 'db.php';

$tds_query = "SELECT tds_value FROM tds_readings ORDER BY reading_time DESC LIMIT 1";
$turbidity_query = "SELECT ntu_value FROM turbidity_readings ORDER BY reading_time DESC LIMIT 1";

$tds_result = $conn->query($tds_query);
$turbidity_result = $conn->query($turbidity_query);

$tds = $tds_result->fetch_assoc()['tds_value'];
$turbidity = $turbidity_result->fetch_assoc()['ntu_value'];

// Call API
$url = "http://localhost:5000/predict?tds={$tds}&turbidity={$turbidity}";
$response = file_get_contents($url);
$data = json_decode($response, true);

echo "Current Water Quality: " . $data['potability_status'];
```

---

## Testing Different Scenarios

### Test 1: Safe Water
```
http://localhost:5000/predict?tds=200&turbidity=0.5
```
Expected: `potability_status: "Potable"`, `potability_score: > 90`

### Test 2: High TDS (Not Safe)
```
http://localhost:5000/predict?tds=600&turbidity=0.8
```
Expected: `potability_status: "Not Potable"`, `potability_score: < 70`

### Test 3: High Turbidity (Not Safe)
```
http://localhost:5000/predict?tds=350&turbidity=2.5
```
Expected: `potability_status: "Not Potable"`, `risk_level: "High"`

### Test 4: Both High (Very Unsafe)
```
http://localhost:5000/predict?tds=800&turbidity=5.0
```
Expected: `potability_status: "Not Potable"`, `potability_score: < 50`

---

## Troubleshooting

### Issue: "Connection refused" or "Python server not responding"
**Solution:**
1. Make sure `ml_server.py` is running:
   ```bash
   python ai/ml_server.py
   ```
2. Check if port 5000 is accessible
3. For production, verify Heroku URL is correct

### Issue: "Invalid parameter format"
**Solution:**
- Make sure all values are numbers
- Check parameter ranges (TDS: 0-10000, Turbidity: 0-100, etc.)

### Issue: CORS errors in browser
**Solution:**
- The API already has CORS headers set
- If still having issues, check browser console for specific error

---

## Quick Test Commands

### Test if server is running:
```bash
curl http://localhost:5000/health
```

### Test prediction:
```bash
curl "http://localhost:5000/predict?tds=350&turbidity=0.8"
```

### Test with all parameters:
```bash
curl "http://localhost:5000/predict?tds=350&turbidity=0.8&temperature=25&ph=7.0"
```

---

That's it! You can now use the API in any way that fits your needs! 🚀


