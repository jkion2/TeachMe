import io
import os
import base64
import google.generativeai as genai
from dotenv import load_dotenv

#load our env variables
load_dotenv()

#global model variables
model = None

def setup_chat_service():
    global model

    #Get an API Key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    #config google AI
    genai.configure(api_key=api_key)

    #Create Model- Change this for whatever AI we use
    
    model = genai.GenerativeModel(
    model_name = 'gemini-2.5-flash',
    generation_config= genai.GenerationConfig(
            temperature=0.7,
            max_output_tokens=2048,
            top_p=0.9,
        )
    )

    print("Chat service initialized with Google AI :)")
    return True

setup_chat_service()


def get_links(image: bytes, context: str) -> dict:
    print("Generating links... inside service_chat.py")
    image_data = {
        'mime_type' : 'image/jpeg',
        'data': base64.b64encode(image).decode('utf-8')
    }

    prompt = f"""
        Analyze this image and the given context to generate relevant educational links.
        
        Context: {context}
        
        Based on what you see in the image and the context provided:
        1. Identify the main topics, subjects, or concepts
        2. Generate 3-5 relevant educational links that would help someone learn more about these topics
        3. Make the links realistic and educational (like Khan Academy, Wikipedia, educational websites)
        
        Return your response in this exact format:
        LINKS:
        - [Topic 1]: http://example-educational-site.com/topic1
        - [Topic 2]: http://another-educational-site.com/topic2
        - [Topic 3]: http://learning-site.com/topic3
        """

    try:
            response = model.generate_content([image_data, prompt])
            ai_response = response.text

            links = parse_links_from_response(ai_response)

            return {"links": links}
    
    except Exception as e:
        return {"error": f"Failed to Generate Links: {str(e)}", "links": []}


def parse_links_from_response(ai_response: str) ->list:
    """Helper function to extract the links from the AI response"""
    links = []

    lines = ai_response.split('\n')

    for line in lines:
        line = line.strip()
        if 'http://' in line or 'https://' in line:
            start = line.find('http')
            if start != -1:
                end = len(line)
                for char in [' ', '\n', '\t', ')']:
                    char_pos = line.find(char, start)
                    if char_pos != -1 and char_pos < end:
                        end = char_pos

                url = line[start:end]
                if url not in links:
                    links.append(url)

    if not links:
        links = [
            "https://www.khanacademy.org/",
            "https://www.coursera.org/",
            "https://www.edx.org/",
        ]                
    return links    




def converse(messages: list[dict]) -> dict:
    
    conversation_text = build_conversation_context(messages)

    try:
        response = model.generate_content(conversation_text)
        ai_response = response.text

        return {"Response": ai_response}
    
    except Exception as e:
        return {"error": f"Failed to generate response: {str(e)}", "response": "Sorry, I couldn't process that request."}

def build_conversation_context(messages: list[dict]) -> str:
    """Helper function to convert message  list  into conversation format"""

    conversation = "You are a helpful educational assistant. Here is the conversation history:\n\n"

    for message in messages:
        role =  message.get('role', 'unknown')
        content = message.get('content', '')

        if role == 'user':
            conversation += f"Student: {content}\n"
        elif role == 'assistant':
            conversation += f"Assistant: {content}\n"
        else:
            conversation += f"Role: {content}\n"

    conversation += "\nAssistant:"

    return conversation


if __name__ == "__main__":
    print("Chat Service is ready!")

    print("Get_links function is ready")
    print("Converse function is ready")

    print("Testing get_links function...")

    from PIL import Image
    import io
    test_img = Image.new('RGB', (100,100), color = 'red')
    img_bytes = io.BytesIO()
    test_img.save(img_bytes, format = 'JPEG')
    image_data = img_bytes.getvalue()

    result = get_links(image_data, "I need help with the math")
    print(f"Result: {result}")


    print("\n🔸 Testing converse function...")
    
    test_messages = [
        {"role": "user", "content": "Hello! Can you help me with math?"}
    ]
    
    result = converse(test_messages)
    print(f"Converse Result: {result}")
    
    # Test with a longer conversation
    print("\n🔸 Testing longer conversation...")
    
    longer_messages = [
        {"role": "user", "content": "What is 2+2?"},
        {"role": "assistant", "content": "2+2 equals 4."},
        {"role": "user", "content": "What about multiplication? What's 3 x 4?"}
    ]
    
    result2 = converse(longer_messages)
    print(f"Longer Conversation Result: {result2}")
    
    # Test the helper function directly
    print("\n🔸 Testing conversation context builder...")
    context = build_conversation_context(longer_messages)
    print(f"Built Context:\n{context}")