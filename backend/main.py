import uvicorn
from fastapi import FastAPI

from service_chat import converse, get_links
from service_manim import generate_manim_video

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/links")
async def links(context: str, image: bytes):
    """Endpoint for getting relevent links based on image and context."""
    return get_links(image, context)


@app.post("/chat")
async def chat(chat_history: list[dict]):
    """Endpoint for handling chat conversations."""
    return converse(chat_history)


@app.post("/manim")
async def manim(context: str, image: bytes):
    """Endpoint for generating a Manim video based on image and context."""
    return generate_manim_video(image, context)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
