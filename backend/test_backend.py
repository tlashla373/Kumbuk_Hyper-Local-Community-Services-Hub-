"""
Quick test script for KumbuK backend
Run this after starting the backend server to verify everything works
"""

import asyncio
import sys

try:
    import httpx
except ImportError:
    print("❌ httpx not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "httpx"])
    import httpx


async def test_backend():
    """Test backend endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("=" * 50)
    print("  KumbuK Backend Test Suite")
    print("=" * 50)
    print()
    
    async with httpx.AsyncClient() as client:
        
        # Test 1: Health Check
        print("[1/3] Testing Health Endpoint...")
        try:
            response = await client.get(f"{base_url}/health")
            if response.status_code == 200:
                print("✓ Health check passed")
                print(f"  Response: {response.json()}")
            else:
                print(f"✗ Health check failed: {response.status_code}")
                return
        except Exception as e:
            print(f"✗ Could not connect to backend: {e}")
            print("  Make sure backend is running on port 8000")
            return
        
        print()
        
        # Test 2: Send Message (Consumer)
        print("[2/3] Testing Consumer Agent...")
        try:
            message_data = {
                "message": "Find me a plumber in Colombo",
                "user_id": "test_consumer_123",
                "session_id": "test_session_001"
            }
            response = await client.post(
                f"{base_url}/message",
                json=message_data
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✓ Consumer agent responded")
                print(f"  Response: {result.get('response', 'No response')[:100]}...")
                if result.get('providers'):
                    print(f"  Found {len(result['providers'])} providers")
            else:
                print(f"✗ Message failed: {response.status_code}")
                print(f"  Error: {response.text}")
        except Exception as e:
            print(f"✗ Error testing consumer agent: {e}")
        
        print()
        
        # Test 3: Send Message (General)
        print("[3/3] Testing General Query...")
        try:
            message_data = {
                "message": "Hello, how can you help me?",
                "user_id": "test_consumer_123",
                "session_id": "test_session_002"
            }
            response = await client.post(
                f"{base_url}/message",
                json=message_data
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✓ General query handled")
                print(f"  Response: {result.get('response', 'No response')[:100]}...")
                if result.get('suggestions'):
                    print(f"  Suggestions: {len(result['suggestions'])} provided")
            else:
                print(f"✗ Query failed: {response.status_code}")
        except Exception as e:
            print(f"✗ Error testing general query: {e}")
    
    print()
    print("=" * 50)
    print("  Test Complete! ✓")
    print("=" * 50)
    print()
    print("Next steps:")
    print("1. Start frontend: nx start consumer-app")
    print("2. Open Expo Go on your phone")
    print("3. Scan QR code and test the chat!")
    print()
    print("API Documentation: http://localhost:8000/docs")
    print()


if __name__ == "__main__":
    print()
    print("Starting backend tests...")
    print("Make sure backend is running: python -m uvicorn app.main:app --reload")
    print()
    
    try:
        asyncio.run(test_backend())
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
