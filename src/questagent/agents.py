from typing import List, Mapping, Any, Dict
import textworld
import textworld.gym.core
import chevron
import openai
from openai import OpenAI


def get_perform_game_action_tool():
    """Get the OpenAI function schema for the perform_game_action tool."""
    return {
        "type": "function",
        "function": {
            "name": "perform_game_action",
            "description": "Execute an action in the text adventure game.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "The command to execute in the game (e.g., 'look', 'go north', 'take sword')"
                    }
                },
                "required": ["action"]
            }
        }
    }


class AgentWithTools(textworld.gym.core.Agent):
    def __init__(self, model_name: str):
        super().__init__()

        self._client = OpenAI()
        self._model_name = model_name
        self._tools = [get_perform_game_action_tool()]

        # Load and render the mustache template
        with open("resources/instructions.mustache", "r") as f:
            template = f.read()
        self._instructions = chevron.render(template, {})

        self._message_history: List[Dict[str, Any]] = []

    def act(self, obs: str, score: int, done: bool, infos: Mapping[str, Any]) -> str:
        print("\n=== OBSERVATION ===")
        print(f"Score: {score}")
        print(f"Done: {done}")
        print(f"Observation: {obs}")
        print("==================\n")

        messages: List[Dict[str, Any]] = [{"role": "system", "content": self._instructions}]
        messages.extend(self._message_history)
        messages.append({"role": "user", "content": obs})

        conversation_turn = 0
        while True:
            conversation_turn += 1
            print(f"--- Conversation Turn {conversation_turn} ---")

            response = self._client.chat.completions.create(
                model=self._model_name,
                messages=messages,
                tools=self._tools,
                tool_choice="auto"
            )

            response_message = response.choices[0].message
            messages.append({
                "role": "assistant",
                "content": response_message.content,
                "tool_calls": response_message.tool_calls
            })

            print(f"LLM Response: {response_message.content}")
            if response_message.tool_calls:
                print(f"Tool calls: {[tc.function.name for tc in response_message.tool_calls]}")

            if response_message.tool_calls:
                action_to_return = None
                for tool_call in response_message.tool_calls:
                    if tool_call.function.name == "perform_game_action":
                        import json
                        args = json.loads(tool_call.function.arguments)
                        action = args["action"]
                        print(f"ACTION DECIDED: {action}")

                        tool_response = {
                            "role": "tool",
                            "content": f"Action '{action}' will be executed in the game.",
                            "tool_call_id": tool_call.id
                        }
                        messages.append(tool_response)

                        if action_to_return is None:
                            action_to_return = action
                    else:
                        tool_response = {
                            "role": "tool",
                            "content": "Tool executed.",
                            "tool_call_id": tool_call.id
                        }
                        messages.append(tool_response)

                if action_to_return:
                    self._message_history.append({"role": "user", "content": obs})
                    self._message_history.extend(messages[len(self._message_history) + 1:])
                    return action_to_return

            if len(messages) > 15:
                print("Adding prompt to encourage action...")
                messages.append({"role": "user", "content": "You must now decide on a specific action to take in the game. Use the perform_game_action tool."})

            continue
