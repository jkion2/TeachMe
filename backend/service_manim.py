import asyncio
from dataclasses import dataclass

import dotenv
from google.genai.types import Blob, Content, Part

from manim_agents import SESSION_ID, USER_ID, prepare_session
from manim_gen import fetch_desired_video
from manim_utils import Timer

dotenv.load_dotenv()


@dataclass
class VideoContext:
    image: str | None = None
    context: str | None = None


def convert_image_to_part(image: str) -> Part:
    # Decode the base64 string to bytes
    image_bytes = image.encode("utf-8")

    # Create a blob from the bytes
    blob = Blob(data=image_bytes, mime_type="image/png")

    # Create a Part object with the blob
    part = Part(inline_data=blob)

    return part


async def invoke_agent(context: VideoContext) -> str:
    # Unpack context
    image = context.image
    additional_context = context.context
    has_image = image is not None
    has_text = additional_context is not None

    # Prepare a session
    with Timer("Prepare Session"):
        runner = await prepare_session()

    # Bundle the context into a Content object
    input_content = None
    if not has_image and not has_text:
        raise ValueError("Either image or context must be provided.")
    elif has_text and not has_image:
        input_content = Content(
            parts=[
                Part(text=additional_context),
            ]
        )
    elif not has_text and has_image:
        input_content = Content(
            parts=[
                convert_image_to_part(image),
            ]
        )
    else:
        input_content = Content(
            parts=[
                convert_image_to_part(image),
                Part(text=additional_context),
            ]
        )

    # Invoke the agent with the provided context
    try:
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=input_content,
        ):
            print(f"Agent took an action: {event.actions}")
        print("Agent actions complete")
    except Exception as e:
        print(f"Agent failed to take an action: {e}")
        print("Video may have been compiled, continuing anyway...")

    # Assume video has already been compiled
    # Get most recent code and video file names
    # If they match, then the video compiled successfully
    # Return the video as a base64 encoded string
    print("Fetching video...")
    video: str = fetch_desired_video()
    return video


async def generate_manim_video(image: str | None, context: str | None) -> str:
    """This functino kicks off the video generation agent with the
    given image and context.

    Args:
        image (bytes): The bytes of the image to be used as context for the video.
        context (str): Additional context or instructions for video generation.

    Returns:
        bytes: The bytes of the generated video.
    """
    if not image and not context:
        raise ValueError("Image and/or context must be provided.")

    with Timer("Invoke Agent"):
        video = await invoke_agent(
            context=VideoContext(
                image=image,
                context=context,
            ),
        )

    return video


if __name__ == "__main__":
    with Timer("Generate Video"):
        asyncio.run(generate_manim_video(None, "Breakdown the equation: y = mx + b."))
