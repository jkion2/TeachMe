"""
Chat service agent implementation using Google ADK for educational problem-solving.
Provides relevant links and conversational AI assistance using agents.
Supports both text and image inputs for problems.
"""

import os
import json
import base64
import io
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from PIL import Image

# Google ADK imports
from google.adk.agents import Agent, LlmAgent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

@dataclass
class Link:
    """Data structure for search result links."""
    title: str
    url: str
    snippet: str
    relevance_score: float = 0.0

# Define the Educational Search Agent
search_agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    instruction="""You are an educational resource finder. When given a math or science problem context, 
    use Google Search to find the most relevant educational resources. Focus on:
    1. Tutorial websites (Khan Academy, PatrickJMT, etc.)
    2. Step-by-step explanations
    3. Educational videos
    4. Interactive learning tools
    5. Practice problems
    
    Format your search queries to include educational terms like "tutorial", "step by step", 
    "how to solve", "explanation", and the specific mathematical concepts.
    
    Respond with an array of JSON objects with {{'title': ..., 'url': ..., 'snippet': ..., 'relevance_score': ...}} for each relevant educational link resource and nothing else so it is easy to parse in python. Please stick to this format strictly and don't put any extra characters at all.""",
    description="An agent specialized in finding educational resources for math and science problems",
    tools=[google_search]
)

# Define the Conversation Tutor Agent
conversation_agent = LlmAgent(
    name="conversation_agent",
    model="gemini-2.0-flash",
    instruction="""You are an expert math and science tutor. Your role is to help students understand problems by:
    1. Breaking down complex concepts into simple, digestible steps
    2. Providing clear explanations with concrete examples
    3. Asking guided questions to check understanding
    4. Offering alternative approaches when students are stuck
    5. Encouraging critical thinking and problem-solving skills
    6. Using analogies and real-world examples to make concepts relatable
    
    Teaching Style Guidelines:
    - Always be patient, encouraging, and supportive
    - Focus on helping students learn the process, not just getting the answer
    - Encourage students to think through problems step-by-step
    - Provide hints rather than direct answers when appropriate
    - Celebrate progress and learning moments
    - Ask follow-up questions to ensure understanding
    
    Keep responses concise but thorough. Adapt your explanations to the student's level of understanding.""",
    description="An expert educational tutor specialized in math and science problem-solving"
)

# Define the Coordinator Agent that manages sub-agents
service_chat_agent = LlmAgent(
    name="service_chat_agent",
    model="gemini-2.0-flash",
    instruction="""You are an educational coordinator that manages learning assistance. 
    You have access to specialized agents:
    1. A search agent that finds educational resources
    2. A tutor agent that provides conversational help
    
    When handling requests:
    - For link requests: delegate to the search agent to find relevant educational resources. Return an array of JSON objects with {{'title': ..., 'url': ..., 'snippet': ..., 'relevance_score': ...}} for each resource and nothing else so it is easy to parse in python. Please stick to this format strictly and don't put any extra characters at all.
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
USER_ID = "ChatServiceAgent"
SESSION_ID = "1"

# Session and Runner
async def setup_session_and_runner():
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=service_chat_agent, app_name=APP_NAME, session_service=session_service)
    return session, runner

# Agent Interaction
async def call_chat_agent(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    session, runner = await setup_session_and_runner()
    
    try:
        events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

        async for event in events:
            if event.is_final_response():
                final_response = event.content.parts[0].text
                return final_response
        
        return ""
    
    except Exception as e:
        print(f"Error in call_chat_agent: {e}")
        return ""

async def get_links(image_data: bytes, context: str) -> List[Dict[str, str]]:
    """
    First endpoint: Get relevant educational links based on text context or image.
    Uses vision agent for image analysis and search agent for finding resources.
    
    Args:
        image_data: Image data in bytes (if provided)
        context: Text description of the problem (if provided)
    
    Returns:
        List of relevant educational links
    """
    print(f"Getting links - Context: {bool(context)}, Image: {bool(image_data)}")
    
    try:
        # Combined context from text and image analysis
        combined_context = context or ""
        
        # If image is provided, analyze it first
        if image_data and len(image_data) > 0:
            combined_context = f"{combined_context}\n\nQuestion/Problem Image Bytes: {image_data}".strip()
        
        # If no context at all, return fallback
        if not combined_context.strip():
            return _get_fallback_links()
        
        # Use the search agent to find educational resources
        search_prompt = f"""Find educational resources for this problem/topic: {combined_context}
        
        Focus on finding:
        1. Tutorial websites and step-by-step guides
        2. Educational videos
        3. Interactive learning tools
        4. Practice problems and examples
        5. Concept explanations
        
        Please search for relevant educational content and return the most helpful resources. Respond with concise web links only to all the resources."""
        
        # Execute search using the agent
        print(f"Calling search agent with prompt: {search_prompt[:100]}...")
        agent_response = await call_chat_agent(search_prompt)

        print(f"Agent response received: {agent_response}")
        
        # Check if we got a valid response
        if not agent_response or len(agent_response.strip()) == 0:
            print("Empty response from agent, using fallback links")
            return _get_fallback_links()
        
        # Parse the agent response to extract links
        result_links = _parse_search_response(agent_response)

        print(f"Parsed links: {result_links}")
        
        # If parsing failed, use fallback
        if not result_links:
            print("No links parsed from response, using fallback")
            return _get_fallback_links()
        
        print(f"Found {len(result_links)} relevant links")
        return result_links
        
    except Exception as e:
        print(f"Error in get_links: {e}")
        return _get_fallback_links()

async def converse(chat_history: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Second endpoint: Handle conversational interaction about the problem.
    Uses the conversation agent for educational tutoring.
    
    Args:
        chat_history: List of chat messages with role and content
    
    Returns:
        Response with AI message, suggestions, and follow-up questions
    """
    print(f"Processing conversation with {len(chat_history)} messages")
    
    try:
        # Extract context from first message if available
        context = ""
        if chat_history and len(chat_history) > 0:
            first_message = chat_history[0].get('content', '')
            if len(first_message) > 50:  # Assume longer first messages contain problem context
                context = first_message
        
        # Build conversation prompt for the tutor agent
        conversation_prompt = _build_conversation_prompt(chat_history, context)
        
        # Use the conversation agent to generate response
        print(f"Calling conversation agent with prompt: {conversation_prompt[:100]}...")
        agent_response = await call_chat_agent(conversation_prompt)
        
        print(f"Conversation agent response: {agent_response}")
        
        # Check if we got a valid response
        if not agent_response or len(agent_response.strip()) == 0:
            print("Empty response from conversation agent, using fallback")
            return {
                "response": "I apologize, but I'm having trouble processing your request right now. Could you please rephrase your question?",
                "suggestions": ["Try breaking down the problem into smaller parts", "What specific concept are you struggling with?"],
                "follow_up_questions": []
            }

        # Process the agent response
        response_data = {
            "response": agent_response,
            "suggestions": ["Try breaking down the problem into smaller parts", "What specific concept are you struggling with?"],
            "follow_up_questions": []
        }
        # response_data = _process_conversation_response(agent_response, chat_history)
        
        print(f"Generated response: {response_data['response'][:100]}...")
        return response_data
        
    except Exception as e:
        print(f"Error in converse: {e}")
        return {
            "response": "I apologize, but I'm having trouble processing your request right now. Could you please rephrase your question?",
            "suggestions": ["Try breaking down the problem into smaller parts", "What specific concept are you struggling with?"],
            "follow_up_questions": []
        }

# Helper functions for agent response processing
def _parse_search_response(agent_response: str) -> List[Dict[str, str]]:
    """Parse the search agent response to extract educational links."""
    # The search agent should return structured information
    # This function processes the agent's response and extracts links
    
    start = agent_response.find('[')
    end = agent_response.rfind(']') + 1
    result_links = json.loads(agent_response[start:end])
    
    # If parsing fails or no links found, return fallback links
    if not result_links:
        result_links = _get_fallback_links()
    
    return result_links

def _get_fallback_links() -> List[Dict[str, str]]:
    """Provide fallback educational links when search fails."""
    fallback_links = [
        {
            "title": "Khan Academy - Math",
            "url": "https://www.khanacademy.org/math",
            "snippet": "Free online math courses and tutorials",
            "relevance": 0.8
        },
        {
            "title": "Wolfram Alpha - Problem Solver",
            "url": "https://www.wolframalpha.com/",
            "snippet": "Computational knowledge engine for math problems",
            "relevance": 0.7
        },
        {
            "title": "PatrickJMT - Math Videos",
            "url": "https://patrickjmt.com/",
            "snippet": "Free math videos and tutorials",
            "relevance": 0.6
        }
    ]

    return fallback_links

def _build_conversation_prompt(chat_history: List[Dict[str, str]], context: str) -> str:
    """Build conversation prompt for the tutor agent."""
    prompt = f"""You are helping a student with a math/science problem. 
    
    Problem Context: {context if context else 'General math/science tutoring'}
    
    Conversation History:
    """
    
    for message in chat_history[-10:]:  # Keep last 10 messages
        role = message.get('role', 'user')
        content = message.get('content', '')
        prompt += f"{role.capitalize()}: {content}\n"
    
    prompt += """
    
    Please provide a helpful, educational response that:
    1. Addresses the student's question or concern
    2. Breaks down complex concepts into simple steps
    3. Encourages understanding rather than just giving answers
    4. Is supportive and patient
    
    Your response should help the student learn and understand the concept better."""
    
    return prompt

def _process_conversation_response(agent_response: str, chat_history: List[Dict[str, str]]) -> Dict[str, Any]:
    """Process the conversation agent response and add suggestions/follow-ups."""
    
    # Generate context-aware suggestions
    suggestions = _generate_suggestions(chat_history, agent_response)
    
    # Generate follow-up questions
    follow_up_questions = _generate_follow_up_questions(agent_response)
    
    return {
        "response": agent_response,
        "suggestions": suggestions,
        "follow_up_questions": follow_up_questions
    }

def _generate_suggestions(chat_history: List[Dict[str, str]], response: str) -> List[str]:
    """Generate helpful suggestions based on conversation context."""
    suggestions = [
        "Can you show me a similar example?",
        "What's the next step in solving this?",
        "How does this relate to what we learned before?",
        "Can you explain this concept differently?",
        "Could you break this down further?",
        "What would happen if I changed one of the variables?"
    ]
    
    # Filter suggestions based on context
    if len(chat_history) > 3:
        suggestions.extend([
            "Can we review what we've covered so far?",
            "How can I apply this to other similar problems?"
        ])
    
    return suggestions[:3]  # Return top 3 suggestions

def _generate_follow_up_questions(response: str) -> List[str]:
    """Generate follow-up questions based on the AI's response."""
    response_lower = response.lower()
    
    if "step" in response_lower:
        return [
            "Does this step make sense to you?", 
            "Would you like me to explain any part in more detail?",
            "Are you ready for the next step?"
        ]
    elif "formula" in response_lower or "equation" in response_lower:
        return [
            "Do you understand how to apply this formula?", 
            "Would you like to try a practice problem?",
            "Can you see where this formula comes from?"
        ]
    elif "example" in response_lower:
        return [
            "Would you like to try a similar problem?",
            "Does this example help clarify the concept?",
            "Can you think of other situations where this applies?"
        ]
    else:
        return [
            "Does this explanation help?", 
            "Do you have any questions about this concept?",
            "Would you like to explore this topic further?"
        ]
