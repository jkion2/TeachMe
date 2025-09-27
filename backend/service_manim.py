import random
from dataclasses import dataclass

from google.adk import Runner
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService

MODEL_NAME = "gemini-2.0-flash"
USER_ID = random.randint(1, 1000000)


@dataclass
class VideoContext:
    image: bytes | None = None
    context: str | None = None


@dataclass
class InvocationDetails:
    session_id: int
    executor: Runner


def initialize_agent() -> InvocationDetails:
    """Initializes the Manim video generation agent with tools and memory.

    Returns:
        Agent: The initialized Manim video generation agent.
    """
    manim_agent = Agent(
        name="Manim_Generator",
        description="Generates a Manim video based on an image and context.",
        model=MODEL_NAME,
        instruction="Talk like a pirate.",
    )

    session_service = InMemorySessionService()
    session_id: int = session_service.create_session(user_id=USER_ID).id
    executor = Runner(session_service=session_service, agent=manim_agent)

    return InvocationDetails(session_id=session_id, executor=executor)


async def initial_code_write(
    video_context: VideoContext, invocation_details: InvocationDetails
) -> str:
    exe = invocation_details.executor
    result = await exe.invoke(query="", session_id=invocation_details.session_id)

    return result.content


def recurrent_code_edit(error: str) -> str: ...


def code_execution(code: str) -> tuple[bool, str]: ...


def invocation_loop(video_context: VideoContext, max_steps: int = 5) -> None:
    # Initialize agent and context
    invoke_details = initialize_agent()

    # Write code

    # Run the code

    # Exit if code works

    # Return error code if it doesn't work

    # Repeat up to max_steps
    pass


def generate_manim_video(image: bytes, context: str) -> bytes:
    """This functino kicks off the video generation agent with the
    given image and context.

    Args:
        image (bytes): The bytes of the image to be used as context for the video.
        context (str): Additional context or instructions for video generation.

    Returns:
        bytes: The bytes of the generated video.
    """
    video_context = VideoContext(image=image, context=context)
    invocation_loop(video_context)

    # Placeholder function to simulate video generation
    return b"FAKE_VIDEO_BYTES"


if __name__ == "__main__":
    generate_manim_video(b"FAKE_IMAGE_BYTES", "FAKE_CONTEXT")
