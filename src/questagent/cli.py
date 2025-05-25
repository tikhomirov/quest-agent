from textworld.helpers import play as textworld_play
from textworld import Agent, Environment, GameState
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class QuestAgent(Agent):
    def act(self, game_state: GameState, reward: float, done: bool) -> str:
        print(game_state.keys())

        system_prompt = f"""
You are an autonomous TextWorld agent.

Goal: {game_state.objective}

Allowed verbs: {', '.join(list(game_state["verbs"]))}

Respond with one valid command per turn, no narration.
"""
        print("*" * 80)
        print("System Prompt:")
        print(system_prompt)
        print("*" * 80)
        print()


        user_prompt = f"""
Observation:
{game_state["description"] if "description" in game_state else "<No description available>"}

Inventory: {game_state["inventory"] if "inventory" in game_state else "<Empty>"}
Score: {game_state["score"]}   Moves: {game_state["moves"]}
Last action: {game_state["last_command"] if "last_command" in game_state else "<None>"}
Last feedback: {game_state["feedback"]}
""" # Visible exits: {extract_exits(state.description)}

        print("*" * 80)
        print("User Prompt:")
        print(user_prompt)
        print("*" * 80)
        print()

        response = openai.responses.create(
            model="gpt-4.1-nano",
            instructions=system_prompt,
            input=[
                {"role": "developer", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            previous_response_id=self._last_response_id
        )

        self._last_response_id = response.id
        action = response.output_text
        print("*" * 80)
        print("Action:")
        print(action)
        print("*" * 80)

        input()

        return action

    def reset(self, env: Environment) -> None:
        self._last_response_id = None

    def finish(self, game_state: GameState, reward: float, done: bool) -> None:
        pass


def main():
    textworld_play('games/test_game.ulx', agent = QuestAgent())

if __name__ == '__main__':
    main()
