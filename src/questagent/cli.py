import argparse
import textworld
from dotenv import load_dotenv
import mlflow
from . import agents

load_dotenv()

def play_episode(game_path: str, model: str, max_steps: int = 50, experiment_name: str = "quest-agent"):
    # Start MLflow run for this episode
    with mlflow.start_run():
        # Log parameters
        mlflow.log_param("game_path", game_path)
        mlflow.log_param("model", model)
        mlflow.log_param("max_steps", max_steps)

        env = textworld.start(game_path)
        agent = agents.AgentWithTools(model_name=model)

        game_state = env.reset()
        obs = game_state.feedback
        infos = game_state.infos or {}

        done = False
        won = False
        total_reward = 0
        steps = 0

        try:
            while not done and steps < max_steps:
                action = agent.act(obs, total_reward, done, infos)

                game_state, reward, done = env.step(action)
                obs = game_state.feedback
                infos = game_state.infos or {}
                total_reward += reward
                steps += 1

                # Log intermediate metrics
                mlflow.log_metric("current_reward", total_reward, step=steps)
                mlflow.log_metric("steps_taken", steps)

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

        # Log final metrics
        mlflow.log_metric("final_reward", total_reward)
        mlflow.log_metric("total_steps", steps)
        mlflow.log_metric("won", 1 if won else 0)
        mlflow.log_metric("completion_rate", steps / max_steps)

        return won, total_reward


def main():
    parser = argparse.ArgumentParser(description="Quest Agent")

    # Required game path
    parser.add_argument("game", type=str, help="Path to game file")

    # Agent configuration
    parser.add_argument("--model", type=str, required=True, help="Model name")
    parser.add_argument("--max-steps", type=int, default=50, help="Maximum number of steps")
    parser.add_argument("--episodes", type=int, default=1, help="Number of episodes to run")

    # MLflow configuration
    parser.add_argument("--experiment-name", type=str, default="quest-agent", help="MLflow experiment name")
    parser.add_argument("--tracking-uri", type=str, help="MLflow tracking URI (optional)")

    args = parser.parse_args()

    # Configure MLflow
    if args.tracking_uri:
        mlflow.set_tracking_uri(args.tracking_uri)

    mlflow.set_experiment(args.experiment_name)

    for episode in range(args.episodes):
        print(f"Episode {episode + 1}/{args.episodes}: ", end="", flush=True)
        won, total_reward = play_episode(
            game_path=args.game,
            model=args.model,
            max_steps=args.max_steps,
            experiment_name=args.experiment_name
        )
        print("won" if won else "lost", end="")
        print(f", reward={total_reward}")


if __name__ == '__main__':
    main()
