"""
Simple API test script to verify the backend is working
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_root():
    """Test root endpoint"""
    print("Testing / endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_chat_message():
    """Test chat message endpoint"""
    print("Testing /api/v1/chat/message endpoint...")
    payload = {
        "message": "I need a plumber in Colombo",
        "session_id": "test_session_123",
        "context": {}
    }
    response = requests.post(f"{BASE_URL}/api/v1/chat/message", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("KUMBUK BACKEND API TEST")
    print("=" * 60)
    print()
    
    try:
        test_health()
        test_root()
        test_chat_message()
        
        print("=" * 60)
        print("✅ All tests completed successfully!")
        print("=" * 60)
        print()
        print("📖 API Documentation: http://localhost:8000/api/docs")
        print("📊 ReDoc: http://localhost:8000/api/redoc")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to backend server.")
        print("Make sure the server is running: python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
