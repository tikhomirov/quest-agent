from typing import Any, Mapping
import textworld
from openai import OpenAI
import os

class OpenAIAgent(textworld.Agent):
    def __init__(self, model_name: str = "gpt-4.1-nano"):
        super().__init__()
        self.model_name = model_name
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self._last_response_id = None
        self._instructions = " ".join(
            [
                "You are an AI agent playing in a text-based adventure game.",
                "Your task is to complete objective of the game that you received at the beginning.",
                "Each step you receive a feedback for your previous action.",
                "In the first step you receive the goal of the game.",
                "You interact with the world by giving commands to the game.",
                "Commands consist of action (verb) and might have target (some object).",
                "You have an inventory that can contain some objects that you pick up during the game.",
                "Your output should consist only of commands that you want to send to the game world."
            ]
        )

    def act(self, game_state: textworld.GameState, reward: float, done: bool) -> str:
        feedback = game_state["feedback"]
        response = self.openai.responses.create(
            model=self.model_name,
            instructions=self._instructions,
            input=[
                {"role": "user", "content": feedback}
            ],
            previous_response_id=self._last_response_id)

        self._last_response_id = response.id
        action = response.output_text
        print(">>> ", action)
        input()
        return action
