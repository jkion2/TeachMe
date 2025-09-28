import random

from google.adk import Runner
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_response import LlmResponse
from google.adk.sessions import InMemorySessionService
from google.adk.tools.agent_tool import AgentTool

from manim_gen import compile_code_to_video, parse_text_to_code, write_code_to_file
from manim_utils import Timer, load_prompt_template

GEMINI_FLASH = "gemini-2.5-flash"
GEMINI_PRO = "gemini-2.5-pro"

USER_ID = str(random.randint(1, 1000000))
SESSION_ID = str(random.randint(1, 1000000))
APP_NAME = "manim-video-generator"


def agent_invoke_callback(callback_context: CallbackContext) -> None:
    agent_name = callback_context.agent_name
    print(f"Agent {agent_name} invoked")


def agent_response_callback(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> None:
    agent_name = callback_context.agent_name
    print(f"Agent {agent_name} responded")

    # Get the response text
    if not llm_response.content:
        raise ValueError("No content found in LLM response")

    if not llm_response.content.parts:
        raise ValueError("No parts found in LLM response")

    if not llm_response.content.parts[0].text:
        raise ValueError("No text found in LLM response")

    response_text = llm_response.content.parts[0].text

    # Write the response text to a file
    code = parse_text_to_code(response_text)
    file_name = write_code_to_file(code)
    print(f"Code written to file: {file_name}")

    # Compile the code to a video
    with Timer("Compile Code to Video"):
        compile_code_to_video(file_name)


def initialize_agent() -> Agent:
    # Math breakdown agent
    math_agent = Agent(
        model=GEMINI_FLASH,
        name="math_agent",
        instruction=load_prompt_template("templates/math.md"),
        before_agent_callback=agent_invoke_callback,
    )

    # Script writing agent
    script_agent = Agent(
        model=GEMINI_FLASH,
        name="script_agent",
        instruction=load_prompt_template("templates/script.md"),
        before_agent_callback=agent_invoke_callback,
    )

    # Video generation agent
    video_agent = Agent(
        model=GEMINI_PRO,
        name="video_agent",
        instruction=load_prompt_template("templates/video.md"),
        before_agent_callback=agent_invoke_callback,
        after_model_callback=agent_response_callback,
    )

    # Orchestrator agent
    orchestrator_agent = Agent(
        model=GEMINI_PRO,
        name="orchestrator_agent",
        instruction=load_prompt_template("templates/orchestrator.md"),
        before_agent_callback=agent_invoke_callback,
        tools=[
            AgentTool(agent=math_agent),
            AgentTool(agent=script_agent),
            AgentTool(agent=video_agent),
        ],
    )

    return orchestrator_agent


async def prepare_session() -> Runner:
    """
    Prepares a session for the agent to use.

    This function initializes the agent and an in-memory session service,
    and then creates a session for the agent to use. The created session
    is then used to create a runner for the agent, which is returned.

    Returns:
        Runner: The runner for the agent.
    """
    with Timer("Initialize Agents"):
        agent = initialize_agent()
    session_service = InMemorySessionService()
    runner = Runner(app_name=APP_NAME, session_service=session_service, agent=agent)
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    return runner
