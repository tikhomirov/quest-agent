import argparse
import textworld.gym.core
import textworld.gym.utils
from dotenv import load_dotenv
from . import agents

load_dotenv()

def play_episode(game: str, model: str, max_steps: int = 50):
    env_id = textworld.gym.utils.register_game(game, max_episode_steps=max_steps)
    env = textworld.gym.utils.make(env_id)

    agent = agents.LangChainGymAgent(model_name=model)

    obs, infos = env.reset()

    done = False
    won = False
    total_reward = 0
    steps = 0

    try:
        while not done and steps < max_steps:
            action = agent.act(obs, total_reward, done, infos)

            obs, reward, done, infos = env.step(action)
            total_reward += reward
            steps += 1

            if "*** The End ***" in obs:
                done = True
                won = True

            if done or infos.get("won", False):
                won = True
                break
            elif infos.get("lost", False):
                break
    finally:
        env.close()

    return won, total_reward


def main():
    parser = argparse.ArgumentParser(description="Quest Agent")
    parser.add_argument("--game", type=str, default="games/test_game.ulx", help="Path the game file")
    parser.add_argument("--model", type=str, default="gpt-4.1-mini", help="Model name")
    parser.add_argument("--max-steps", type=int, default=50, help="Maximum number of steps")
    parser.add_argument("--episodes", type=int, default=1, help="Maximum number of steps")

    args = parser.parse_args()

    for episode in range(args.episodes):
        print(f"Episode {episode}/{args.episodes}: ", end="", flush=True)
        won, total_reward = play_episode(game=args.game, model=args.model, max_steps=args.max_steps)
        print("won" if won else "lost", end="")
        print(f", reward={total_reward}")


if __name__ == '__main__':
    main()
