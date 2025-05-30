import json
from os import path
from typing import Tuple

from langchain import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory

from ChatInterface import ChatInterface

user_data_dir = path.join(
    path.abspath(path.dirname(__file__)),
    '..',
    'user_files'
)

settings_path = path.join(user_data_dir, 'settings.json')


class ChatAIWithoutDocuments(ChatInterface):
    def __init__(self, verbose=False):
        temperature = 0.2
        model_name = 'gemini-2.0-flash'
        with open(settings_path, 'r') as f:
            data = json.load(f)
            temperature = data['temperature']
            model_name = data['llmModel']

        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)
        self.memory = ConversationBufferMemory()
        self.conversationChain = ConversationChain(llm=self.llm, memory=self.memory, verbose=verbose)

    def human_message(self, query: str) -> Tuple[str, None]:
        return self.conversationChain.predict(input=query), None

    def clear_memory(self):
        self.memory.clear()
