from .prompts import system_prompt, user_prompt
from .retrieval import build_context
from .config import GEN_MODEL

def answer_question(client_id: str, question: str, history=None, on_token=None):
    if history is None:
        history = []
    context, cites = build_context(client_id, question)
    messages = [{"role": "system", "content": system_prompt(client_id)}]

    messages += history

    messages.append({"role": "user", "content": user_prompt(question, context)})

    from .chat import stream_chat

    reply = stream_chat(GEN_MODEL, messages, on_token=on_token, echo=(on_token is None))

    if cites.strip():

        reply = f"{reply}\n\nИсточники: {cites}"

    history.append({"role": "user", "content": question})

    history.append({"role": "assistant", "content": reply})

    return reply, history

