"""
Test script for RAMate API
"""
import requests
import json

def test_chat_api():
    """Test the chat API endpoint"""
    try:
        response = requests.post(
            'http://localhost:5000/api/chat',
            headers={'Content-Type': 'application/json'},
            json={
                'query': 'What should I do during emergency evacuations?',
                'session_id': 'test_session'
            },
            timeout=30
        )
        
        print(f'Status: {response.status_code}')
        
        if response.status_code == 200:
            result = response.json()
            print(f'Response status: {result.get("status")}')
            
            if result.get('status') == 'success' and 'data' in result:
                data = result['data']
                print(f'\nQuery: {data.get("query")}')
                print(f'\nAnswer:\n{data.get("answer", "")}')
                print(f'\nSources: {data.get("sources", [])}')
                print(f'Confidence: {data.get("confidence", 0):.3f}')
                print(f'Links: {data.get("links", [])}')
            else:
                print(f'Message: {result.get("message")}')
        else:
            print(f'Error response: {response.text}')
            
    except Exception as e:
        print(f'Error testing API: {str(e)}')

def test_system_status():
    """Test the system status endpoint"""
    try:
        response = requests.get('http://localhost:5000/api/status')
        print(f'System Status: {response.status_code}')
        
        if response.status_code == 200:
            result = response.json()
            if 'data' in result:
                data = result['data']
                print(f'Vector store: {data.get("vector_store_status")}')
                print(f'Total documents: {data.get("total_documents")}')
                print(f'OpenRouter configured: {data.get("openrouter_configured")}')
                print(f'Source files: {len(data.get("source_files", []))}')
            
    except Exception as e:
        print(f'Error checking status: {str(e)}')

if __name__ == "__main__":
    print("🧪 Testing RAMate API...")
    print("=" * 50)
    
    # Test system status first
    test_system_status()
    print("\n" + "=" * 50)
    
    # Test chat functionality
    test_chat_api()
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")
