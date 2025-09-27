import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from service_chat import converse, get_links
from service_manim import generate_manim_video
from get_da_link import get_da_link

from pydantic import BaseModel

class LinkRequest(BaseModel):
    context: str
    image: str  # Placeholder string for the image data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # For local testing with a Chrome Extension, allowing all origins is often necessary.
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  # <--- Ensures OPTIONS, POST, GET, etc. are allowed
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/kushlinks")
async def kushlinks(data: LinkRequest):
    prompt = data.context
    print(f"--- API HIT: /kushlinks ---")
    print(f"Prompt received: {prompt[:50]}...")

    agent_response = await get_da_link(prompt)
    print(f"Agent response received: {agent_response['summary_text'][:50]}...")

    summary = agent_response['summary_text']
    html_links = agent_response['search_html']
    print(f"Rendered HTML received: {html_links[:50]}...")
    print(f"summary received: {summary[:50]}...")
    return {
        "text": summary,
        "html_links": html_links,
        "source": "ADK Agent with Google Search"
    }

# @app.post("/links")
# async def links(data: LinkRequest):
#     # --- New Logging ---
#     print(f"--- API HIT: /links ---")
#     print(f"Context received: {data.context[:50]}...")
#     print(f"Image string received: {data.image}")
#     # --- End Logging ---
#     dummy_image_bytes = b""
#     result_links = get_links(dummy_image_bytes, data.context)
#     print(f"Links generated: {result_links}")
#     """Endpoint for getting relevent links based on image and context."""
#     return {"links": result_links}


@app.post("/chat")
async def chat(chat_history: list[dict]):
    """Endpoint for handling chat conversations."""
    return converse(chat_history)


@app.post("/manim")
async def manim(context: str, image: str):
    """Endpoint for generating a Manim video based on image and context."""
    return generate_manim_video(image, context)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
