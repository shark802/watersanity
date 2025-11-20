# How to Integrate ML API into Water Potability Dashboard

## File Location
`field_worker_water_potability_dashboard.php` (line 129)

## Integration Options

### Option 1: Call Your PHP Bridge (Recommended)

Replace any existing API calls on line 129 with:

```php
// Get potability recommendation from ML API
function getPotabilityFromML($tds, $turbidity, $temperature = 25, $ph = 7.0) {
    // Use your PHP bridge that connects to Heroku
    $api_url = '../api/python_ml_server.php'; // Adjust path as needed
    
    $url = $api_url . '?tds=' . $tds . '&turbidity=' . $turbidity . 
           '&temperature=' . $temperature . '&ph=' . $ph;
    
    $response = @file_get_contents($url);
    
    if ($response === false) {
        return [
            'status' => 'error',
            'message' => 'ML API not available'
        ];
    }
    
    return json_decode($response, true);
}

// Usage on line 129 or nearby:
$tds_value = $row['tds_value'] ?? 350; // Get from database
$turbidity_value = $row['turbidity_value'] ?? 0.8; // Get from database

$ml_result = getPotabilityFromML($tds_value, $turbidity_value);

if ($ml_result['status'] === 'success') {
    $potability_status = $ml_result['potability_status'];
    $potability_score = $ml_result['potability_score'];
    $recommendation = $ml_result['recommendation'];
    $risk_level = $ml_result['risk_level'];
} else {
    // Fallback if API fails
    $potability_status = 'Unknown';
    $potability_score = 0;
    $recommendation = 'Unable to get AI recommendation';
}
```

### Option 2: Direct JavaScript Call (Frontend)

If line 129 is in JavaScript, use:

```javascript
// Line 129 or in your JavaScript section
async function getPotabilityRecommendation(tds, turbidity) {
    try {
        const response = await fetch(
            '../api/python_ml_server.php?tds=' + tds + '&turbidity=' + turbidity
        );
        const data = await response.json();
        
        if (data.status === 'success') {
            // Update UI
            document.getElementById('potability-status').textContent = data.potability_status;
            document.getElementById('potability-score').textContent = data.potability_score + '%';
            document.getElementById('recommendation').textContent = data.recommendation;
            
            return data;
        }
    } catch (error) {
        console.error('Error calling ML API:', error);
    }
}

// Usage
getPotabilityRecommendation(350, 0.8);
```

### Option 3: AJAX Call (jQuery)

If you're using jQuery:

```javascript
// Line 129 or in script section
$.ajax({
    url: '../api/python_ml_server.php',
    method: 'GET',
    data: {
        tds: 350,
        turbidity: 0.8,
        temperature: 25,
        ph: 7.0
    },
    dataType: 'json',
    success: function(data) {
        if (data.status === 'success') {
            $('#potability-status').text(data.potability_status);
            $('#potability-score').text(data.potability_score + '%');
            $('#recommendation').text(data.recommendation);
        }
    },
    error: function(xhr, status, error) {
        console.error('ML API Error:', error);
    }
});
```

## Common Issues on Line 129

### Issue 1: API Path Incorrect
**Fix:** Adjust the path to `python_ml_server.php`:
```php
// If file is in: /main/field_worker_water_potability_dashboard.php
// And API is in: /api/python_ml_server.php
$api_url = '../../api/python_ml_server.php';
```

### Issue 2: CORS Error
**Fix:** The API already has CORS headers, but if issues persist:
```php
// In python_ml_server.php (already done, but verify)
header('Access-Control-Allow-Origin: *');
```

### Issue 3: API Not Responding
**Fix:** Add error handling:
```php
$context = stream_context_create([
    'http' => [
        'timeout' => 5,
        'ignore_errors' => true
    ]
]);

$response = @file_get_contents($url, false, $context);
```

## Complete Integration Example

Here's a complete example you can use around line 129:

```php
<?php
// Around line 129 in field_worker_water_potability_dashboard.php

// Function to get ML recommendation
function getMLPotability($tds, $turbidity) {
    $api_url = '../../api/python_ml_server.php'; // Adjust path
    
    $url = $api_url . '?tds=' . floatval($tds) . 
           '&turbidity=' . floatval($turbidity);
    
    $context = stream_context_create([
        'http' => [
            'timeout' => 5,
            'ignore_errors' => true
        ]
    ]);
    
    $response = @file_get_contents($url, false, $context);
    
    if ($response === false) {
        return null;
    }
    
    return json_decode($response, true);
}

// In your loop where you display water quality data:
while ($row = $water_quality_result->fetch_assoc()):
    $tds = $row['tds_value'] ?? 350;
    $turbidity = $row['turbidity_value'] ?? 0.8;
    
    // Get ML recommendation
    $ml_result = getMLPotability($tds, $turbidity);
    
    if ($ml_result && $ml_result['status'] === 'success'):
        $potability_status = $ml_result['potability_status'];
        $potability_score = $ml_result['potability_score'];
        $recommendation = $ml_result['recommendation'];
        $risk_level = $ml_result['risk_level'];
    else:
        // Fallback
        $potability_status = 'Unknown';
        $potability_score = 0;
        $recommendation = 'AI analysis unavailable';
        $risk_level = 'Unknown';
    endif;
    
    // Display the results
    ?>
    <tr>
        <td><?php echo $potability_status; ?></td>
        <td><?php echo $potability_score; ?>%</td>
        <td><?php echo $recommendation; ?></td>
    </tr>
    <?php
endwhile;
?>
```

## Testing

After integration, test with:

1. **Check browser console** for JavaScript errors
2. **Check PHP error logs** for server-side errors
3. **Test API directly:**
   ```
   https://your-domain.com/api/python_ml_server.php?tds=350&turbidity=0.8
   ```

## Need More Help?

If you can share:
- The exact error message
- What's on line 129
- What you're trying to do

I can provide a more specific solution!


