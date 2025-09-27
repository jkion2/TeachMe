def get_links(image: bytes, context: str) -> dict:
    """This function triggers the chat agent with the given image and context.
    The agent processes the image and context to generate relevant links.

    Args:
        image (bytes): The bytes of the image to be processed.
        context (str): Additional context or instructions for link generation.

    Returns:
        dict: A dictionary containing the generated links.
    """

    # Placeholder function to simulate link generation
    return {"links": ["http://example.com/link1", "http://example.com/link2"]}


def converse(messages: list[dict]) -> dict:
    """This function handles a conversation with the chat agent.

    Args:
        messages (list[dict]): A list of message dictionaries,
            each containing 'role' and 'content'.

    Returns:
        dict: A dictionary containing the agent's response.
    """

    # Placeholder function to simulate conversation
    return {"response": "This is a simulated response from the chat agent."}
