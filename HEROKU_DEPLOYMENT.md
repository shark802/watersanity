# Heroku Deployment Guide

This guide will help you deploy the Water Potability AI Server to Heroku.

## Prerequisites

1. **Heroku Account**: Sign up at [heroku.com](https://www.heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Ensure Git is installed and configured
4. **Trained Models**: Make sure you have trained the ML models before deploying

## Step 1: Prepare Your Models

Before deploying, ensure your trained model files exist in the `ai/` directory:
- `potability_classifier.pkl`
- `potability_score_regressor.pkl`

If you haven't trained them yet, run:
```bash
cd ai
python train_potability_recommendation.py
```

## Step 2: Initialize Git Repository (if not already done)

```bash
cd C:\Users\cjsar\Desktop\watersanity
git init
git add .
git commit -m "Initial commit - Ready for Heroku deployment"
```

## Step 3: Login to Heroku

```bash
heroku login
```

This will open a browser window for authentication.

## Step 4: Create Heroku App

```bash
heroku create your-app-name
```

Replace `your-app-name` with your desired app name (must be unique). For example:
```bash
heroku create water-potability-ai
```

## Step 5: Deploy to Heroku

```bash
git push heroku main
```

If your default branch is `master` instead of `main`:
```bash
git push heroku master
```

## Step 6: Verify Deployment

After deployment, check if your app is running:
```bash
heroku open
```

Or test the health endpoint:
```bash
curl https://your-app-name.herokuapp.com/health
```

## Step 7: Check Logs

Monitor your application logs:
```bash
heroku logs --tail
```

## Important Notes

### Model Files
- **IMPORTANT**: Make sure your `.pkl` model files are committed to Git (they should be in the `ai/` directory)
- Heroku's filesystem is ephemeral, but files committed to Git are included in the deployment
- If models are too large (>100MB), consider using Heroku's external storage or a CDN

### Environment Variables
If you need to set environment variables (e.g., database credentials):
```bash
heroku config:set VARIABLE_NAME=value
```

### Scaling
To scale your app (if needed):
```bash
heroku ps:scale web=1
```

### Updating Your App
After making changes:
```bash
git add .
git commit -m "Your commit message"
git push heroku main
```

## API Endpoints

Once deployed, your API will be available at:
- `https://your-app-name.herokuapp.com/` - Home/Info
- `https://your-app-name.herokuapp.com/health` - Health check
- `https://your-app-name.herokuapp.com/status` - Server status
- `https://your-app-name.herokuapp.com/predict?tds=350&turbidity=0.8` - Get prediction (GET)
- `https://your-app-name.herokuapp.com/predict` - Get prediction (POST)
- `https://your-app-name.herokuapp.com/test` - Test endpoint

## Example Usage

### GET Request
```bash
curl "https://your-app-name.herokuapp.com/predict?tds=350&turbidity=0.8&temperature=25&ph=7.0"
```

### POST Request
```bash
curl -X POST https://your-app-name.herokuapp.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "tds_value": 350,
    "turbidity_value": 0.8,
    "temperature": 25,
    "ph_level": 7.0
  }'
```

## Troubleshooting

### Models Not Loading
If you see errors about models not loading:
1. Check that model files exist in `ai/` directory
2. Verify files are committed to Git
3. Check logs: `heroku logs --tail`

### App Crashes
1. Check logs: `heroku logs --tail`
2. Verify all dependencies are in `requirements.txt`
3. Ensure Python version in `runtime.txt` is supported by Heroku

### Port Issues
The app automatically uses Heroku's `PORT` environment variable. No configuration needed.

### Build Failures
1. Check `requirements.txt` for correct package versions
2. Verify `Procfile` syntax is correct
3. Check `runtime.txt` for valid Python version

## Updating PHP Bridge

After deploying to Heroku, update your PHP bridge file (`api/python_ml_server.php`) to use the Heroku URL:

```php
// Replace this line:
$python_server_url = 'http://localhost:5000';

// With your Heroku URL:
$python_server_url = 'https://your-app-name.herokuapp.com';
```

## Free Tier Limitations

Heroku's free tier has been discontinued. You'll need to use a paid plan:
- **Eco Dyno**: $5/month per dyno (recommended for development)
- **Basic Dyno**: $7/month per dyno

For production, consider:
- **Standard Dynos**: Better performance and reliability
- **Add-ons**: For databases, monitoring, etc.

## Support

For more information, visit:
- [Heroku Python Support](https://devcenter.heroku.com/articles/python-support)
- [Heroku Getting Started](https://devcenter.heroku.com/articles/getting-started-with-python)

