from typing import List
from langchain_community.chat_models import ChatOllama

def customer_service_chatbot(messages: List[dict]) -> dict:
    system_message = {
        "role": "system",
        "content": "You are a customer support agent for an airline.",
    }
    messages = [system_message] + messages
    llm = ChatOllama(model="llama3.1:8b", format="json", temperature=0)
    response = llm.generate([{"role": "user", "content": message["content"]} for message in messages])
    return {"content": response.generations[0][0].text.strip()}