from typing import List
import textworld
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langchain.memory import ConversationBufferMemory

class LangChainAgent(textworld.Agent):
    def __init__(self, model_name: str = "gpt-4.1-mini"):
        super().__init__()

        self._llm = ChatOpenAI(
            model=model_name,
            use_responses_api=True
        )

        template = PromptTemplate.from_file(
            template_file="resources/instructions.mustache",
            template_format="mustache"
        )
        self._instructions = template.format(name="QuestAgent")

        self._memory = ConversationBufferMemory(return_messages=True)

    def act(self, game_state: textworld.GameState, reward: float, done: bool) -> str:
        feedback = game_state["feedback"]

        messages: List[BaseMessage] = [SystemMessage(content=self._instructions)]

        if hasattr(self._memory, "chat_memory") and self._memory.chat_memory.messages:
            messages.extend(self._memory.chat_memory.messages)

        messages.append(HumanMessage(content=feedback))

        response = self._llm.invoke(messages)
        action = response.text()

        self._memory.chat_memory.add_user_message(feedback)
        self._memory.chat_memory.add_ai_message(action)

        input("$ " + action)

        return action
