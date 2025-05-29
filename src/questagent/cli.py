from textworld.helpers import play as textworld_play
from dotenv import load_dotenv
from . import agents

load_dotenv()

def main():
    textworld_play('games/test_game.ulx', agent = agents.OpenAIAgent(), max_nb_steps=50)

if __name__ == '__main__':
    main()
