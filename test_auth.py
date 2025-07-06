#!/usr/bin/env python3
"""
Simple authentication test script
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_auth():
    print("🔐 Testing Authentication Process")
    print("=" * 50)
    
    # Step 1: Login to get token
    print("1. Logging in...")
    login_data = {
        "username": "erkanyy",  # Change this to your username
        "password": "Eycursor1234."  # Change this to your password
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/token",
            data=login_data
        )
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data['access_token']
            print(f"✅ Login successful!")
            print(f"   Token: {token[:50]}...")
            print(f"   Token type: {token_data['token_type']}")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    print("\n" + "-" * 50)
    
    # Step 2: Test authorization with token
    print("2. Testing authorization...")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers=headers
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print("✅ Authorization successful!")
            print(f"   Username: {user_data.get('username')}")
            print(f"   Email: {user_data.get('email')}")
            print(f"   Role: {user_data.get('role')}")
            print(f"   First Name: {user_data.get('first_name')}")
            print(f"   Last Name: {user_data.get('last_name')}")
        else:
            print(f"❌ Authorization failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Authorization error: {e}")
    
    print("\n" + "-" * 50)
    
    # Step 3: Test admin dashboard access
    print("3. Testing admin dashboard access...")
    try:
        response = requests.get(
            f"{BASE_URL}/admin/dashboard",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✅ Dashboard access successful!")
        else:
            print(f"❌ Dashboard access failed: {response.status_code}")
            print(f"   Error: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Dashboard access error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Authentication test completed!")

if __name__ == "__main__":
    test_auth() 