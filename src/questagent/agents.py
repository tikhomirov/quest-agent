from typing import List, Optional, Dict, Any
import textworld
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langchain.memory import ConversationBufferMemory

class LangChainAgent(textworld.Agent):
    def __init__(self, model_name: str = "o4-mini", reasoning_effort: str = "medium", reasoning_summary: Optional[str] = "auto"):
        super().__init__()

        reasoning = {
            "effort": reasoning_effort,
            "summary": reasoning_summary
        }

        self._llm = ChatOpenAI(
            model=model_name,
            use_responses_api=True,
            model_kwargs={"reasoning": reasoning},
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

        response = self._llm.invoke(messages, store=True)

        self._extract_and_display_reasoning(response)

        action = response.text()
        input("$ " + action)

        self._memory.chat_memory.add_user_message(feedback)
        self._memory.chat_memory.add_ai_message(action)

        return action

    def _extract_and_display_reasoning(self, response) -> None:
        if hasattr(response, 'additional_kwargs') and 'reasoning' in response.additional_kwargs:
            reasoning = response.additional_kwargs['reasoning']
            self._last_reasoning = reasoning

            print("Reasoning:")
            print("-" * 50)

            if 'summary' in reasoning:
                for block in reasoning['summary']:
                    if 'text' in block:
                        print(f"• {block['text']}")

            print("-" * 50)
