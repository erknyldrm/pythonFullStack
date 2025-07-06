#!/usr/bin/env python3
"""
Test script for admin registration endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_admin_registration():
    """Test the enhanced admin registration endpoint"""
    
    print("🧪 Testing Admin Registration Endpoints")
    print("=" * 50)
    
    # Test data for registration
    test_user = {
        "username": "testadmin",
        "email": "testadmin@example.com",
        "password": "SecurePass123!",
        "confirm_password": "SecurePass123!",
        "first_name": "Test",
        "last_name": "Admin",
        "role": "admin"
    }
    
    # Test 1: Basic registration
    print("1. Testing basic admin registration...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Registration successful!")
            print(f"   User: {result['user']['username']}")
            print(f"   Email: {result['user']['email']}")
            print(f"   Role: {result['user']['role']}")
            print(f"   Message: {result['message']}")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "-" * 50)
    
    # Test 2: Login with registered user
    print("2. Testing login with registered user...")
    try:
        login_data = {
            "username": test_user["username"],
            "password": test_user["password"]
        }
        
        response = requests.post(
            f"{BASE_URL}/auth/token",
            data=login_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login successful!")
            print(f"   Token: {result['access_token'][:20]}...")
            token = result['access_token']
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            token = None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        token = None
    
    print("\n" + "-" * 50)
    
    # Test 3: Get user profile
    if token:
        print("3. Testing get user profile...")
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Profile retrieved successfully!")
                print(f"   Username: {result['username']}")
                print(f"   Email: {result['email']}")
                print(f"   Role: {result['role']}")
                print(f"   First Name: {result['first_name']}")
                print(f"   Last Name: {result['last_name']}")
            else:
                print(f"❌ Profile retrieval failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "-" * 50)
    
    # Test 4: Test password validation
    print("4. Testing password validation...")
    weak_password_user = {
        "username": "weakuser",
        "email": "weak@example.com",
        "password": "weak",
        "confirm_password": "weak",
        "role": "admin"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=weak_password_user,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 400:
            result = response.json()
            print("✅ Password validation working!")
            print(f"   Error: {result['detail']}")
        else:
            print(f"❌ Password validation failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "-" * 50)
    
    # Test 5: Test duplicate username
    print("5. Testing duplicate username validation...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 400:
            result = response.json()
            print("✅ Duplicate validation working!")
            print(f"   Error: {result['detail']}")
        else:
            print(f"❌ Duplicate validation failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Registration endpoint testing completed!")

def test_invitation_system():
    """Test the invitation system (requires admin token)"""
    
    print("\n🧪 Testing Invitation System")
    print("=" * 50)
    
    # First, login as admin to get token
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/token", data=login_data)
        if response.status_code == 200:
            token = response.json()['access_token']
            print("✅ Admin login successful")
            
            # Test invitation creation
            invitation_data = {
                "email": "invited@example.com",
                "role": "moderator"
            }
            
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                f"{BASE_URL}/auth/invite",
                json=invitation_data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Invitation created successfully!")
                print(f"   Email: {result['email']}")
                print(f"   Role: {result['role']}")
                print(f"   Invitation ID: {result['invitation_id'][:20]}...")
                print(f"   Expires: {result['expires_at']}")
                
                # Test registration with invitation
                invited_user = {
                    "username": "inviteduser",
                    "email": "invited@example.com",
                    "password": "SecurePass123!",
                    "confirm_password": "SecurePass123!",
                    "first_name": "Invited",
                    "last_name": "User",
                    "role": "moderator"
                }
                
                response = requests.post(
                    f"{BASE_URL}/auth/register/invited?invitation_id={result['invitation_id']}",
                    json=invited_user,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print("✅ Invited user registration successful!")
                    print(f"   User: {result['user']['username']}")
                    print(f"   Role: {result['user']['role']}")
                else:
                    print(f"❌ Invited registration failed: {response.status_code}")
                    print(f"   Error: {response.text}")
                    
            else:
                print(f"❌ Invitation creation failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        else:
            print("❌ Admin login failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_admin_registration()
    test_invitation_system() 