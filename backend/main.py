import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from service_chat import converse, get_links
from service_manim import generate_manim_video

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


@app.post("/links")
async def links(data: LinkRequest):
    # --- New Logging ---
    print(f"--- API HIT: /links ---")
    print(f"Context received: {data.context[:50]}...")
    print(f"Image string received: {data.image}")
    # --- End Logging ---
    dummy_image_bytes = b""
    result_links = get_links(dummy_image_bytes, data.context)
    """Endpoint for getting relevent links based on image and context."""
    return {"links": result_links}


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
