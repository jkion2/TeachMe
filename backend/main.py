import uvicorn
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
import base64
import io
import json

from service_chat import converse, get_links
from service_manim import generate_manim_video

import dotenv

dotenv.load_dotenv()

from pydantic import BaseModel


class ChatRequest(BaseModel):
    chat_history: List[Dict[str, str]]


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


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
async def links(
    context: Optional[str] = Form(""), image: Optional[UploadFile] = File(None)
):
    """Endpoint for getting relevant educational links based on text context or image."""
    try:
        print(f"--- API HIT: /links ---")
        print(f"Text context received: {context[:50] if context else 'None'}...")
        print(f"Image file received: {image.filename if image else 'No'}")

        # Process uploaded image if provided
        image_bytes = b""
        if image:
            try:
                image_bytes = await image.read()
                print(f"Read image size: {len(image_bytes)} bytes")
            except Exception as img_error:
                print(f"Error reading image file: {img_error}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to read image file: {str(img_error)}",
                )

        # Validate input - must have either text or image
        if not context and not image:
            raise HTTPException(
                status_code=400, detail="Must provide either text context or image file"
            )

        # Get relevant links using the search agent
        result_links = await get_links(image_bytes, context or "")
        result_links = result_links[: min(len(result_links), 5)]

        print(f"Returning {len(result_links)} links")
        return {"links": result_links, "status": "success"}

    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        print(f"Error in /links endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch links: {str(e)}")


@app.post("/chat")
async def chat(data: ChatRequest):
    """Endpoint for handling chat conversations about educational problems."""
    try:
        print(f"--- API HIT: /chat ---")
        print(f"Chat history length: {len(data.chat_history)}")

        # Validate chat history format
        for i, message in enumerate(data.chat_history):
            if (
                not isinstance(message, dict)
                or "role" not in message
                or "content" not in message
            ):
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid message format at index {i}. Expected dict with 'role' and 'content' keys.",
                )

        # Process conversation using the conversation agent
        response_data = await converse(data.chat_history)

        print(f"Generated response length: {len(response_data.get('response', ''))}")
        return {**response_data, "status": "success"}

    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        print(f"Error in /chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process chat: {str(e)}")


@app.post("/manim")
async def manim(context: str = Form(...), image: UploadFile = File(...)):
    """Endpoint for generating a Manim video based on uploaded image and context."""
    try:
        print(f"--- API HIT: /manim ---")
        print(f"Context received: {context[:50]}...")
        print(f"Image file received: {image.filename}")

        # Read the uploaded image
        try:
            image_bytes: bytes = await image.read()
            print(f"Read image size: {len(image_bytes)} bytes")
        except Exception as img_error:
            print(f"Error reading image file: {img_error}")
            raise HTTPException(
                status_code=400, detail=f"Failed to read image file: {str(img_error)}"
            )

        encoded_image: str = base64.b64encode(image_bytes).decode("utf-8")

        # Generate video using the manim service
        print("Generating Manim video...")
        result: str = await generate_manim_video(encoded_image, context)

        print(f"Generated video size: {len(result)} bytes")
        print("Returning Manim video...")
        return {"video_data": result, "status": "success"}

    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        print(f"Error in /manim endpoint: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to generate video: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
