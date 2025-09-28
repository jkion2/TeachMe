#!/usr/bin/env python3
"""
Test script for the TeachMe chat service endpoints using Google ADK.
Run this after setting up your environment variables.
"""

import requests
import json
import os
from typing import Dict, Any
import dotenv

dotenv.load_dotenv()

# Configuration
BASE_URL = "http://localhost:8000"

def test_links_endpoint():
    """Test the /links endpoint with a sample math problem."""
    print("🔗 Testing /links endpoint...")
    
    # Prepare form data instead of JSON
    form_data = {
        "context": "I need help solving quadratic equations like x^2 + 5x + 6 = 0. I'm struggling to understand the factoring method and would like to see step-by-step examples."
    }
    
    try:
        response = requests.post(f"{BASE_URL}/links", data=form_data, timeout=300)
        response.raise_for_status()
        
        data = response.json()
        print(data)
        print(f"✅ Success! Found {len(data.get('links', []))} links")
        
        for i, link in enumerate(data.get('links', [])[:3], 1):
            print(f"  {i}. {link.get('title', 'N/A')}")
            print(f"     URL: {link.get('url', 'N/A')}")
            print(f"     Snippet: {link.get('snippet', 'N/A')[:100]}...")
            print()
            
    except requests.exceptions.Timeout:
        print("⏱️  Request timed out. The ADK search might be taking longer than expected.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")

def test_chat_endpoint():
    """Test the /chat endpoint with a sample conversation."""
    print("💬 Testing /chat endpoint...")
    
    test_chat_history = {
        "chat_history": [
            {
                "role": "user",
                "content": "I'm working on quadratic equations and I got stuck on x^2 + 5x + 6 = 0. Can you help me understand how to factor this?"
            }
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/chat", json=test_chat_history, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print("✅ Success! AI Response:")
        print(f"Response: {data.get('response', 'No response')}")
        print(f"Suggestions: {data.get('suggestions', [])}")
        print(f"Follow-up questions: {data.get('follow_up_questions', [])}")
        
    except requests.exceptions.Timeout:
        print("⏱️  Request timed out. The ADK agent might be taking longer than expected.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")

def test_conversation_flow():
    """Test a multi-turn conversation."""
    print("🔄 Testing multi-turn conversation...")
    
    conversation = [
        {
            "role": "user",
            "content": "I need to solve x^2 - 7x + 12 = 0 using factoring."
        }
    ]
    
    for turn in range(2):  # Test 2 turns
        print(f"\n--- Turn {turn + 1} ---")
        
        try:
            response = requests.post(f"{BASE_URL}/chat", json={"chat_history": conversation}, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            ai_response = data.get('response', '')
            
            print(f"AI: {ai_response[:200]}...")
            
            # Add AI response to conversation
            conversation.append({
                "role": "assistant", 
                "content": ai_response
            })
            
            # Add a follow-up question
            follow_up = "Can you show me another example?" if turn == 0 else "What if the equation doesn't factor nicely?"
            conversation.append({
                "role": "user",
                "content": follow_up
            })
            
        except requests.exceptions.Timeout:
            print(f"⏱️  Turn {turn + 1} timed out.")
            break
        except requests.exceptions.RequestException as e:
            print(f"❌ Error in turn {turn + 1}: {e}")
            break

def check_server_status():
    """Check if the server is running."""
    print("🏥 Checking server status...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        response.raise_for_status()
        print("✅ Server is running!")
        return True
    except requests.exceptions.RequestException:
        print("❌ Server is not running. Please start it with: uvicorn main:app --reload")
        return False

def check_environment():
    """Check if required environment variables are set."""
    print("🔧 Checking environment variables...")
    
    required_vars = ['GOOGLE_API_KEY']
    optional_vars = ['GOOGLE_CLOUD_PROJECT_ID']
    
    all_good = True
    
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"❌ {var} is not set (required for Google ADK)")
            all_good = False
    
    for var in optional_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"⚠️  {var} is not set (optional)")
    
    return all_good

def main():
    """Run all tests."""
    print("🚀 TeachMe Chat Service Test Suite (Google ADK)")
    print("=" * 60)
    
    # Check environment
    env_ok = check_environment()
    if not env_ok:
        print("\n⚠️  Some environment variables are missing. The service may not work properly.")
        print("Please check .env.example for required variables.")
        return
    
    # Check server status
    if not check_server_status():
        return
    
    print("\n" + "=" * 60)
    print("⚠️  Note: ADK agents may take longer to respond than traditional APIs")
    print("=" * 60)
    
    # Run tests
    test_links_endpoint()
    print("\n" + "-" * 40)
    test_chat_endpoint()
    print("\n" + "-" * 40)
    test_conversation_flow()
    
    print("\n🎉 Test suite completed!")
    print("\n💡 Tips for using Google ADK:")
    print("   - Agents may take 10-30 seconds to respond initially")
    print("   - The google_search tool provides comprehensive results")
    print("   - Multi-agent coordination provides better responses")

if __name__ == "__main__":
    main()
