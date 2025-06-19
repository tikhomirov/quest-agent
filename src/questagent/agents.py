from typing import List, Mapping, Any
import textworld
import textworld.gym.core
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage, AIMessage, ToolMessage
from langchain_core.tools import tool


@tool
def perform_game_action(action: str) -> str:
    """Execute an action in the text adventure game.

    Args:
        action: The command to execute in the game (e.g., 'look', 'go north', 'take sword')

    Returns:
        A confirmation that the action will be executed
    """
    return f"Executing action: {action}"


class LangChainGymAgent(textworld.gym.core.Agent):
    def __init__(self, model_name: str):
        super().__init__()

        self._llm = ChatOpenAI(
            model=model_name,
        )
        self._llm_with_tools = self._llm.bind_tools([perform_game_action])

        template = PromptTemplate.from_file(
            template_file="resources/instructions.mustache",
            template_format="mustache"
        )
        self._instructions = template.format()

        self._message_history: List[BaseMessage] = []

    def act(self, obs: str, score: int, done: bool, infos: Mapping[str, Any]) -> str:
        print("\n=== OBSERVATION ===")
        print(f"Score: {score}")
        print(f"Done: {done}")
        print(f"Observation: {obs}")
        print("==================\n")

        messages: List[BaseMessage] = [SystemMessage(content=self._instructions)]
        messages.extend(self._message_history)
        messages.append(HumanMessage(content=obs))

        conversation_turn = 0
        while True:
            conversation_turn += 1
            print(f"--- Conversation Turn {conversation_turn} ---")

            response = self._llm_with_tools.invoke(messages)
            messages.append(response)

            print(f"LLM Response: {response.content}")
            if isinstance(response, AIMessage) and response.tool_calls:
                print(f"Tool calls: {[tc['name'] for tc in response.tool_calls]}")

            if isinstance(response, AIMessage) and response.tool_calls:
                action_to_return = None
                for tool_call in response.tool_calls:
                    if tool_call["name"] == "perform_game_action":
                        action = tool_call["args"]["action"]
                        print(f"ACTION DECIDED: {action}")

                        tool_response = ToolMessage(
                            content=f"Action '{action}' will be executed in the game.",
                            tool_call_id=tool_call["id"]
                        )
                        messages.append(tool_response)

                        if action_to_return is None:
                            action_to_return = action
                    else:
                        tool_response = ToolMessage(
                            content="Tool executed.",
                            tool_call_id=tool_call["id"]
                        )
                        messages.append(tool_response)

                if action_to_return:
                    self._message_history.append(HumanMessage(content=obs))
                    self._message_history.extend(messages[len(self._message_history) + 1:])
                    return action_to_return

            if len(messages) > 15:
                print("Adding prompt to encourage action...")
                messages.append(HumanMessage(content="You must now decide on a specific action to take in the game. Use the perform_game_action tool."))

            continue
