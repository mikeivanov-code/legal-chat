def system_prompt(client_id: str) -> str:
    return (
        "You are a meticulous legal assistant. Answer ONLY based on the information provided to you and the chat history.\n"
        "If the answer is not in the provided information — say that you don’t know.\n"
        "Hallucinations are not allowed. \n"
        f"Клиент: {client_id}\n"
        "At the end, include sources in the format [filename:chunk]."
    )

def user_prompt(question: str, context: str) -> str:
    return (
        f"Вопрос: {question}\n\n"
        f"КОНТЕКСТ:\n{context}\n\n"
        "Give a brief, precise answer in English."
    )
