#!/usr/bin/env python3
"""
Test script for TeachMe chat service with image support.
Tests both text and image inputs for the enhanced endpoints.
"""

import requests
import json
import os
import base64
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"

def create_test_image():
    """Create a simple test image with a math problem."""
    from PIL import Image, ImageDraw, ImageFont
    import io
    
    # Create a simple image with a math equation
    img = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    # Draw a simple math problem
    text = "Solve: x² + 5x + 6 = 0"
    draw.text((20, 80), text, fill='black', font=font)
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def test_links_with_text():
    """Test /links endpoint with text input."""
    print("📝 Testing /links endpoint with text...")
    
    test_data = {
        "context": "I need help solving quadratic equations like x^2 + 5x + 6 = 0. I want to understand factoring methods.",
        "image_base64": ""
    }
    
    try:
        response = requests.post(f"{BASE_URL}/links", json=test_data, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Success! Found {len(data.get('links', []))} links")
        
        for i, link in enumerate(data.get('links', [])[:2], 1):
            print(f"  {i}. {link['title'][:60]}...")
            print(f"     URL: {link['url']}")
            print()
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_links_with_image():
    """Test /links endpoint with image input."""
    print("🖼️  Testing /links endpoint with image...")
    
    try:
        # Create test image
        image_bytes = create_test_image()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        test_data = {
            "context": "",
            "image_base64": f"data:image/png;base64,{image_base64}"
        }
        
        response = requests.post(f"{BASE_URL}/links", json=test_data, timeout=45)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Success! Found {len(data.get('links', []))} links from image")
        
        for i, link in enumerate(data.get('links', [])[:2], 1):
            print(f"  {i}. {link['title'][:60]}...")
            print(f"     URL: {link['url']}")
            print()
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_links_upload_endpoint():
    """Test /links/upload endpoint with file upload."""
    print("📤 Testing /links/upload endpoint...")
    
    try:
        # Create test image
        image_bytes = create_test_image()
        
        files = {
            'image': ('test_math.png', image_bytes, 'image/png')
        }
        data = {
            'text': 'This image contains a quadratic equation'
        }
        
        response = requests.post(f"{BASE_URL}/links/upload", files=files, data=data, timeout=45)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Success! Found {len(result.get('links', []))} links from upload")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def test_chat_with_image():
    """Test /chat/with-image endpoint."""
    print("💬🖼️ Testing /chat/with-image endpoint...")
    
    try:
        # Create test image
        image_bytes = create_test_image()
        
        chat_history = [
            {
                "role": "user",
                "content": "Can you help me understand this quadratic equation in the image?"
            }
        ]
        
        files = {
            'image': ('math_problem.png', image_bytes, 'image/png')
        }
        data = {
            'chat_history': json.dumps(chat_history)
        }
        
        response = requests.post(f"{BASE_URL}/chat/with-image", files=files, data=data, timeout=45)
        response.raise_for_status()
        
        result = response.json()
        print("✅ Success! AI Response:")
        print(f"  Image analyzed: {result.get('image_analyzed', False)}")
        print(f"  Response: {result.get('response', 'No response')[:200]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def test_mixed_input():
    """Test with both text and image."""
    print("🔗🖼️ Testing /links endpoint with both text and image...")
    
    try:
        image_bytes = create_test_image()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        test_data = {
            "context": "I'm struggling with quadratic equations. The image shows a specific problem I need help with.",
            "image_base64": f"data:image/png;base64,{image_base64}"
        }
        
        response = requests.post(f"{BASE_URL}/links", json=test_data, timeout=45)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Success! Found {len(data.get('links', []))} links using text + image context")
        
    except Exception as e:
        print(f"❌ Error: {e}")

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
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print("✅ GOOGLE_API_KEY is set")
        return True
    else:
        print("❌ GOOGLE_API_KEY is not set (required for Google ADK)")
        return False

def main():
    """Run all tests for image and text support."""
    print("🚀 TeachMe Chat Service Test Suite - Image & Text Support")
    print("=" * 70)
    
    # Check prerequisites
    env_ok = check_environment()
    if not env_ok:
        print("\n⚠️  Environment setup incomplete.")
        return
    
    if not check_server_status():
        return
    
    print("\n" + "=" * 70)
    print("⚠️  Note: Vision analysis may take 30-60 seconds")
    print("=" * 70)
    
    # Run tests
    test_links_with_text()
    print("\n" + "-" * 50)
    
    test_links_with_image()
    print("\n" + "-" * 50)
    
    test_mixed_input()
    print("\n" + "-" * 50)
    
    test_links_upload_endpoint()
    print("\n" + "-" * 50)
    
    test_chat_with_image()
    
    print("\n" + "=" * 70)
    print("🎉 Test suite completed!")
    print("\n💡 Available endpoints:")
    print("   • POST /links - Text or base64 image input")
    print("   • POST /links/upload - Direct file upload")
    print("   • POST /chat - Text conversation")
    print("   • POST /chat/with-image - Conversation with image support")

if __name__ == "__main__":
    main()
