from openai import OpenAI

class ChatBuilder:
    def __init__(self, messages : list | None = None) -> None:
        self._messages = messages or []
    
    def system_message(self, content: str):
        self._messages.append({"role": "system", "content": content})
        return self
    
    def user_message(self, content: str):
        self._messages.append({"role": "user", "content": content})
        return self
    
    def assistant_message(self, content: str):
        self._messages.append({"role": "assistant", "content": content})
        return self
    
    def build(self):
        return self._messages
    
def remove_quotes_if_string_is_in_quotes(text: str):
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    return text

def ask(question: str, history: list | None = []) -> tuple[list, str]:
    client = OpenAI()

    builder = ChatBuilder(history)
    
    if not history:
        builder.system_message("You are a chatbot that answers questions in a short and consise manner.")
    
    messages = builder.user_message(question).build()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        n=1,
    )

    content_results = [
        remove_quotes_if_string_is_in_quotes(c.message.content.strip())
        for c in response.choices
    ]

    builder.assistant_message(content_results[-1])

    return builder.build(), content_results[-1]
