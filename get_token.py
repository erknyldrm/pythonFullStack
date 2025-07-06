#!/usr/bin/env python3
"""
Get a fresh token for Swagger UI authorization
"""

import requests

BASE_URL = "http://localhost:8000"

def get_token():
    print("🔑 Getting fresh token for Swagger UI...")
    print("=" * 50)
    
    login_data = {
        "username": "erkanyy",  # Change to your username
        "password": "Eycursor1234."  # Change to your password
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/token",
            data=login_data
        )
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data['access_token']
            
            print("✅ Token obtained successfully!")
            print("\n📋 Copy this for Swagger UI Authorize:")
            print("=" * 50)
            print(f"Bearer {token}")
            print("=" * 50)
            print("\n📝 Instructions:")
            print("1. Click 'Authorize' button in Swagger UI")
            print("2. Paste the above text in the Value field")
            print("3. Click 'Authorize' then 'Close'")
            
        else:
            print(f"❌ Failed to get token: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    get_token() 