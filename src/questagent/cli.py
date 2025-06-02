import argparse
from textworld.helpers import play as textworld_play
from dotenv import load_dotenv
from . import agents

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Quest Agent with OpenAI Reasoning")
    parser.add_argument("--game", default="games/test_game.ulx", help="Game file to play")
    parser.add_argument("--max-steps", type=int, default=50, help="Maximum number of steps")

    args = parser.parse_args()

    agent = agents.LangChainAgent()

    textworld_play(args.game, agent=agent, max_nb_steps=args.max_steps)

if __name__ == '__main__':
    main()
