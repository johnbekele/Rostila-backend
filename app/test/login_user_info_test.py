import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class LoginUserInfoTest:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.headers = {"Content-Type": "application/json"}
        self.token = None
        
    def test_login(self, email, password):
        """Test login endpoint and get access token"""
        print("🔐 Testing Login Endpoint...")
        print(f"Email: {email}")
        print(f"Password: {'*' * len(password)}")
        
        login_data = {
            "email": email,
            "password": password
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json=login_data,
                headers=self.headers
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("token")
                print("✅ Login successful!")
                print(f"Access Token: {self.token[:50]}...")
                print(f"Token Type: {data.get('token_type')}")
                return True
            else:
                print("❌ Login failed!")
                print(f"Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Login request failed: {e}")
            return False
    
    def test_user_info(self):
        """Test user-info endpoint with access token"""
        if not self.token:
            print("❌ No access token available. Please login first.")
            return False
            
        print("\n👤 Testing User Info Endpoint...")
        print(f"Using token: {self.token[:50]}...")
        
        auth_headers = {
            **self.headers,
            "Authorization": f"Bearer {self.token}"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/user-info",
                headers=auth_headers
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ User info retrieved successfully!")
                print("User Data:")
                print(f"  ID: {data.get('id')}")
                print(f"  Username: {data.get('username')}")
                print(f"  Email: {data.get('email')}")
                print(f"  First Name: {data.get('first_name')}")
                print(f"  Last Name: {data.get('last_name')}")
                print(f"  Is Verified: {data.get('is_verified')}")
                print(f"  Created At: {data.get('created_at')}")
                print(f"  Updated At: {data.get('updated_at')}")
                return True
            else:
                print("❌ User info request failed!")
                print(f"Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ User info request failed: {e}")
            return False
    
    def test_find_user(self):
        """Test find/user endpoint with access token"""
        if not self.token:
            print("❌ No access token available. Please login first.")
            return False
            
        print("\n🔍 Testing Find User Endpoint...")
        print(f"Using token: {self.token[:50]}...")
        
        auth_headers = {
            **self.headers,
            "Authorization": f"Bearer {self.token}"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/find/user",
                headers=auth_headers
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Find user successful!")
                print("User Data:")
                print(f"  ID: {data.get('id')}")
                print(f"  Username: {data.get('username')}")
                print(f"  Email: {data.get('email')}")
                print(f"  First Name: {data.get('first_name')}")
                print(f"  Last Name: {data.get('last_name')}")
                print(f"  Is Verified: {data.get('is_verified')}")
                return True
            else:
                print("❌ Find user request failed!")
                print(f"Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Find user request failed: {e}")
            return False
    
    def run_full_test(self, email, password):
        """Run complete test suite"""
        print("=" * 60)
        print("🚀 Starting Complete Auth Test Suite")
        print("=" * 60)
        
        # Test 1: Login
        login_success = self.test_login(email, password)
        
        if not login_success:
            print("\n❌ Login failed. Cannot proceed with other tests.")
            return False
        
        # Test 2: User Info
        user_info_success = self.test_user_info()
        
        # Test 3: Find User
        find_user_success = self.test_find_user()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Test Results Summary")
        print("=" * 60)
        print(f"Login: {'✅ PASS' if login_success else '❌ FAIL'}")
        print(f"User Info: {'✅ PASS' if user_info_success else '❌ FAIL'}")
        print(f"Find User: {'✅ PASS' if find_user_success else '❌ FAIL'}")
        
        all_passed = login_success and user_info_success and find_user_success
        print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
        
        return all_passed

def main():
    print("🔧 Auth Test Suite")
    print("This will test login and user-info endpoints")
    print()
    
    # Get credentials from user
    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()
    
    if not email or not password:
        print("❌ Email and password are required!")
        return
    
    # Run tests
    tester = LoginUserInfoTest()
    tester.run_full_test(email, password)

if __name__ == "__main__":
    main()
