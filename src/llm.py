import base64
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

_client: OpenAI | None = None

def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found. Please set it in your .env file.")
        _client = OpenAI(api_key=api_key)
    return _client

def _encode_image(image_path: Path) -> str:
    """Encodes an image file to a base64 string for the Vision API."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def _get_image_media_type(image_path: Path) -> str:
    ext = image_path.suffix.lower()
    return {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png"}.get(ext.lstrip("."), "image/png")

def chat(
    messages: list[dict],
    system_prompt: str,
    model: str = "gpt-4o",
    json_mode: bool = False,
) -> str:
    """
    Sends a multi-turn chat request to the LLM.

    Args:
        messages: List of {"role": "user"/"assistant", "content": ...} dicts.
        system_prompt: The agent's system prompt defining its role.
        model: The OpenAI model to use.
        json_mode: If True, forces the response to be valid JSON.

    Returns:
        The assistant's reply as a string.
    """
    client = _get_client()

    full_messages = [{"role": "system", "content": system_prompt}] + messages

    kwargs: dict = {"model": model, "messages": full_messages}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content or ""

def chat_with_image(
    messages: list[dict],
    system_prompt: str,
    image_path: Path,
    model: str = "gpt-4o",
) -> str:
    """
    Sends a chat request that includes an image (Vision).
    The image is prepended to the first user message in the conversation.

    Args:
        messages: List of {"role": "user"/"assistant", "content": ...} dicts.
                  The first message should be the user's query about the image.
        system_prompt: The agent's system prompt.
        image_path: Path to the image file to include.
        model: The OpenAI model to use (must support Vision).

    Returns:
        The assistant's reply as a string.
    """
    client = _get_client()

    encoded = _encode_image(image_path)
    media_type = _get_image_media_type(image_path)

    # Inject the image into the first user message
    messages_with_image = list(messages)
    if messages_with_image and messages_with_image[0]["role"] == "user":
        first_text = messages_with_image[0]["content"]
        messages_with_image[0] = {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{media_type};base64,{encoded}"},
                },
                {"type": "text", "text": first_text},
            ],
        }

    full_messages = [{"role": "system", "content": system_prompt}] + messages_with_image

    response = client.chat.completions.create(model=model, messages=full_messages)
    return response.choices[0].message.content or ""
