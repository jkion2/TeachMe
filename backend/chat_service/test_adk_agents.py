#!/usr/bin/env python3
"""
Quick test to verify Google ADK agents are working correctly.
This tests the core agent functionality before running the full server.
"""

import os
import asyncio
import dotenv
from google.adk.agents import Agent, LlmAgent
from google.adk.tools import google_search
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools.agent_tool import AgentTool

dotenv.load_dotenv()

# Create search agent
search_agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash-exp",
    instruction="""You are an educational resource finder. Find relevant educational links for math and science problems. Respond with concise web links only to all the resources.""",
    description="An agent specialized in finding educational resources",
    tools=[google_search]
)

# Create conversation agent
conversation_agent = LlmAgent(
    name="conversation_agent",
    model="gemini-2.0-flash-exp",
    instruction="""You are a helpful math tutor. Help students understand mathematical concepts step by step.""",
    description="An expert educational tutor"
)

# Define the Coordinator Agent that manages sub-agents
service_chat_agent = LlmAgent(
    name="service_chat_agent",
    model="gemini-2.0-flash-exp",
    instruction="""You are an educational coordinator that manages learning assistance. 
    You have access to specialized agents:
    1. A search agent that finds educational resources
    2. A tutor agent that provides conversational help
    
    When handling requests:
    - For link requests: delegate to the search agent to find relevant educational resources. Return an array of JSON objects with {{'title': ..., 'url': ..., 'snippet': ..., 'relevance_score': ...}} for each resource and nothing else so it is easy to parse in python.
    - For conversations: delegate to the tutor agent for educational discussions
    - Always maintain context about the educational problem being discussed""",
    description="Coordinates educational assistance between search and tutoring agents",
    tools=[
        AgentTool(agent=search_agent),
        AgentTool(agent=conversation_agent),
    ]
)


# Instantiate constants
APP_NAME = "TeachMe"
USER_ID = "12345"
SESSION_ID = "123344"

# Session and Runner
async def setup_session_and_runner():
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=service_chat_agent, app_name=APP_NAME, session_service=session_service)
    return session, runner


# Agent Interaction
async def call_agent_async(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    session, runner = await setup_session_and_runner()
    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    async for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response: ", final_response)




async def main():
    """Run direct ADK agent tests."""
    print("🚀 Google ADK Agent Test")
    print("=" * 40)
    
    # Check environment
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found. Please set it in your .env file")
        return
    
    print("✅ GOOGLE_API_KEY found")
    print("=" * 40)
    
    # Test agents
    search_success = await call_agent_async("Find educational resources for solving quadratic equations")
    print("-" * 40)
    conversation_success = await call_agent_async("Explain how to factor x^2 + 5x + 6")
    print("=" * 40)
    
    if search_success and conversation_success:
        print("🎉 All ADK agents working correctly!")
        print("💡 You can now run the full server with: uvicorn main:app --reload")
    else:
        print("⚠️  Some agents failed. Check your API key and internet connection.")

if __name__ == "__main__":
    asyncio.run(main())
