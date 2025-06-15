from typing import List, Mapping, Any
import textworld
import textworld.gym.core
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage


class LangChainGymAgent(textworld.gym.core.Agent):
    def __init__(self, model_name: str):
        super().__init__()

        self._llm = ChatOpenAI(
            model=model_name,
        )

        template = PromptTemplate.from_file(
            template_file="resources/instructions.mustache",
            template_format="mustache"
        )
        self._instructions = template.format()

        self._message_history: List[BaseMessage] = []

    def act(self, obs: str, score: int, done: bool, infos: Mapping[str, Any]) -> str:
        context = obs

        messages: List[BaseMessage] = [SystemMessage(content=self._instructions)]
        messages.extend(self._message_history)
        messages.append(HumanMessage(content=obs))

        response = self._llm.invoke(messages)
        if isinstance(response.content, list) and response.content:
            action = str(response.content[0]).strip()
        else:
            action = str(response.content).strip()

        self._message_history.append(HumanMessage(content=context))
        self._message_history.append(response)

        return action
