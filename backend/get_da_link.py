# get_da_link.py

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types

# Constants for the session (can be hardcoded for a single-session backend)
APP_NAME = "educational_search_agent"
USER_ID = "student_user"
SESSION_ID = "current_session"

# Define the ADK Agent (uses the provided logic)
root_agent = Agent(
    name="educational_link_finder",
    model="gemini-2.5-flash",  # Gemini 2.5 is compatible with google_search tool
    description="Agent to find relevant educational links for a student's study prompt.",
    instruction="You are a helpful study assistant. Use the Google Search tool to find and summarize 3-5 high-quality, relevant educational links (like Khan Academy, Coursera, official guides, etc.) based on the user's prompt. After providing the summary and links, always conclude your text response with a placeholder tag '##ADK_RESPONSE_END##'.",
    tools=[google_search]
)

# Setup Session and Runner
async def setup_session_and_runner():
    """Initializes the session service and runner for the agent."""
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
    return session, runner

# Agent Interaction Function
async def get_da_link(query: str):
    """
    Calls the ADK agent with a query and returns the final response text 
    and the rendered search HTML.
    """
    content = types.Content(role='user', parts=[types.Part(text=query)])
    
    session, runner = await setup_session_and_runner()
    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    final_text = ""
    rendered_html = ""
    
    async for event in events:
        if event.is_final_response():
            # Iterate through ALL parts in the final response content
            for part in event.content.parts:
                
                # Check for the main text part
                if part.text and not final_text:
                    final_text = part.text
                    
                # 🎯 FIX: Use Python's built-in function hasattr() to safely check for the attribute
                # The rendered_content (HTML) might be on a tool-specific Part object.
                if hasattr(part, 'rendered_content') and part.rendered_content:
                    rendered_html = part.rendered_content
            
            # Since we found the final response, we can stop processing events
            break 

    # We return both the raw text summary and the required HTML to the endpoint
    return {
        "summary_text": final_text,
        "search_html": rendered_html
    }