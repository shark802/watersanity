#!/usr/bin/env python3
"""
Quick test script to verify Heroku setup before deployment
Run this to check if everything is configured correctly
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} NOT FOUND: {filepath}")
        return False

def check_model_files():
    """Check if model files exist"""
    ai_dir = os.path.join(os.path.dirname(__file__), 'ai')
    classifier = os.path.join(ai_dir, 'potability_classifier.pkl')
    regressor = os.path.join(ai_dir, 'potability_score_regressor.pkl')
    
    classifier_exists = check_file_exists(classifier, "Potability Classifier")
    regressor_exists = check_file_exists(regressor, "Score Regressor")
    
    return classifier_exists and regressor_exists

def main():
    print("=" * 60)
    print("Heroku Deployment Setup Check")
    print("=" * 60)
    print()
    
    all_good = True
    
    # Check required files
    print("📋 Checking required files...")
    print()
    
    files_to_check = [
        ('requirements.txt', 'Python dependencies file'),
        ('Procfile', 'Heroku Procfile'),
        ('runtime.txt', 'Python runtime version'),
        ('.gitignore', 'Git ignore file'),
        ('ai/ml_server.py', 'Main Flask application'),
    ]
    
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_good = False
    
    print()
    print("🤖 Checking ML model files...")
    print()
    
    if not check_model_files():
        all_good = False
        print()
        print("⚠️  WARNING: Model files not found!")
        print("   You need to train the models before deploying:")
        print("   cd ai && python train_potability_recommendation.py")
        print()
    
    # Check requirements.txt content
    print()
    print("📦 Checking requirements.txt...")
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
            required_packages = ['Flask', 'gunicorn', 'joblib', 'numpy', 'pandas', 'scikit-learn']
            for package in required_packages:
                if package.lower() in content.lower():
                    print(f"   ✅ {package} found")
                else:
                    print(f"   ❌ {package} NOT FOUND")
                    all_good = False
    except Exception as e:
        print(f"   ❌ Error reading requirements.txt: {e}")
        all_good = False
    
    # Check Procfile
    print()
    print("📄 Checking Procfile...")
    try:
        with open('Procfile', 'r') as f:
            content = f.read()
            if 'gunicorn' in content and 'ml_server:app' in content:
                print("   ✅ Procfile looks correct")
            else:
                print("   ❌ Procfile may be incorrect")
                all_good = False
    except Exception as e:
        print(f"   ❌ Error reading Procfile: {e}")
        all_good = False
    
    # Summary
    print()
    print("=" * 60)
    if all_good:
        print("✅ All checks passed! Ready for Heroku deployment.")
        print()
        print("Next steps:")
        print("1. git init (if not already done)")
        print("2. git add .")
        print("3. git commit -m 'Ready for Heroku'")
        print("4. heroku create your-app-name")
        print("5. git push heroku main")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
    print("=" * 60)

if __name__ == '__main__':
    main()

