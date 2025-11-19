import ollama
from typing import List, Dict, Callable, Optional




def stream_chat(model: str, messages: List[Dict[str, str]], on_token: Optional[Callable[[str], None]] = None, echo: bool = True):
    """Stream tokens from Ollama. If on_token is provided, call it for each token.

    echo=True will also print tokens to stdout."""

    stream = ollama.chat(
        model=model,
        messages=messages,
        stream=True,
        options={
            "temperature": 0.8
        }
    )
    reply = ""

    for chunk in stream:

        content = ""

        try:

            content = chunk.get("message", {}).get("content", "")

        except Exception:

            content = ""

        if not content:

            continue

        if on_token is not None:

            try:

                on_token(content)

            except Exception:

                # GUI callbacks may fail if widget destroyed; ignore to keep stream alive

                pass

        if echo:

            print(content, end="", flush=True)

        reply += content

    if echo:

        print()

    return reply

